from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Literal

app = FastAPI(
    title="GigHub API",
    description="API for managing freelance gigs in Nairobi.\nAdmission Number: C027-01-0898/2024",
    version="1.0.0",
    docs_url="/",
    redoc_url=None,        # disable ReDoc
    openapi_url="/openapi.json"
)

gigs_db = [
   {
	"id": 1,
	"title": "Project Requirements & Roadmap",
	"description": "Define scope, goals, milestones, and deliverables for the development work.",
	"category": "Development",
	"budget": 5000.0,
	"currency": "KES",
	"status": "In Progress",
	"client_name": "Acme Labs"
   },
   {
	"id": 2,
	"title": "API Development (Core Endpoints)",
	"description": "Implement core REST endpoints, request validation, and basic error handling.",
	"category": "Development",
	"budget": 12000.0,
	"currency": "KES",
	"status": "In Progress",
	"client_name": "BluePeak Solutions"
  },
  {
    "id": 3,
    "title": "Database & Data Modeling",
    "description": "Design schema, relationships, and seed data for the application.",
    "category": "Development",
    "budget": 8000.0,
    "currency": "KES",
    "status": "Closed",
    "client_name": "Nairobi FinTech Co."
  },
  {
    "id": 4,
    "title": "Frontend Integration",
    "description": "Integrate UI with backend APIs and ensure consistent data formats.",
    "category": "Development",
    "budget": 9500.0,
    "currency": "KES",
    "status": "Open",
    "client_name": "GreenGate Media"
  },
  {
    "id": 5,
    "title": "Testing & Bug Fixing Sprint",
    "description": "Unit tests, integration tests, and fixing issues found during QA.",
    "category": "Development",
    "budget": 7000.0,
    "currency": "KES",
    "status": "In Progress",
    "client_name": "Orbit Systems"
  },
  {
    "id": 6,
    "title": "UX Wireframes for Key Screens",
    "description": "Create wireframes for onboarding, dashboard, and details pages aligned to user flows.",
    "category": "Design ",
    "budget": 30000.0,
    "currency": "KES",
    "status": "Open",
    "client_name": "SilverPeak Tech"
  },
  {
    "id": 7,
    "title": "UI Design & Component Styling",
    "description": "Design UI components, spacing, typography, and consistent styling across the product.",
    "category": "Design",
    "budget": 42000.0,
    "currency": "KES",
    "status": "Closed",
    "client_name": "Harbor Analytics"
  },
  {
    "id": 8,
    "title": "Website Copy & Landing Page Messaging",
    "description": "Write marketing and product copy for the landing page including headlines and CTA text.",
    "category": "Writing",
    "budget": 25000.0,
    "currency": "KES",
    "status": "Closed",
    "client_name": "Vertex Ventures"
  },
  {
    "id": 9,
    "title": "User Help Content & Microcopy",
    "description": "Create error messages, tooltips, FAQs structure, and onboarding microcopy.",
    "category": "writing",
    "budget": 28000.0,
    "currency": "KES",
    "status": "In Progress",
    "client_name": "Kilimani Edu"
  },
  {
    "id": 10,
    "title": "Testing, Bug Fixes & Deployment Prep",
    "description": "Write tests, to be used on the system for production deployment.",
    "category": "Writing",
    "budget": 70000.0,
    "currency": "KES",
    "status": "Open",
    "client_name": "Coastline Services"
  },
  {
    "id": 11,
    "title": "Product Documentation Draft",
    "description": "Draft documentation sections, endpoint descriptions, and a basic user guide outline.",
    "category": "Design",
    "budget": 22000.0,
    "currency": "KES",
    "status": "Open",
    "client_name": "BrightDesk Co."
  },
  {
    "id": 12,
    "title": "User Guide Draft",
    "description": "Draft documentation content and a basic user guide structure.",
    "category": "Writing",
    "budget": 5200.0,
    "currency": "KES",
    "status": "In Progress",
    "client_name": "Kilimani Edu"
  },
  {
    "id": 13,
    "title": "Final UI Polish & Handoff Notes",
    "description": "Polish final UI screens and provide developer handoff notes and usage guidance.",
    "category": "Design",
    "budget": 35000.0,
    "currency": "KES",
    "status": "In Progress",
    "client_name": "Union Studio"
  }
]
class GigCreate(BaseModel):
    title: str = Field(min_length=5, max_length=100)
    description: str = Field(min_length=20, max_length=500)
    category: Literal["Development", "Design", "Writing"]
    budget: float = Field(gt=0)
    client_name: str = Field(min_length=2, max_length=50)


class GigUpdate(BaseModel):
    budget: Optional[float] = Field(None, gt=0)
    status: Optional[Literal["Open", "In Progress", "Closed"]] = None



@app.get("/gigs")
def list_gigs():
    """
    Return all gigs.
    """
    return gigs_db




@app.get("/gigs/{gig_id}")
def get_gig(gig_id: int):
    """
    Return a single gig by ID.
    """
    for gig in gigs_db:
        if gig["id"] == gig_id:
            return gig

    raise HTTPException(status_code=404, detail="Gig not found")


@app.get("/gigs/search")
def search_gigs(q: str):
    """
    Search gigs by title.
    """
    results = []

    for gig in gigs_db:
        if q.lower() in gig["title"].lower():
            results.append(gig)

    return results



@app.post("/gigs")
def create_gig(gig: GigCreate):
    """
    Create a new gig.
    """

    new_id = max([g["id"] for g in gigs_db]) + 1

    new_gig = {
        "id": new_id,
        "title": gig.title,
        "description": gig.description,
        "category": gig.category,
        "budget": gig.budget,
        "currency": "KES",
        "status": "Open",
        "client_name": gig.client_name
    }

    gigs_db.append(new_gig)

    return {
        "message": "Gig created successfully",
        "gig": new_gig
    }
@app.put("/gigs/{gig_id}")
def update_gig(gig_id: int, gig_update: GigUpdate):
    """
    Update a gig's budget or status.
    """

    for index, gig in enumerate(gigs_db):

        if gig["id"] == gig_id:

            if gig_update.budget is not None:
                gigs_db[index]["budget"] = gig_update.budget

            if gig_update.status is not None:
                gigs_db[index]["status"] = gig_update.status

            return {
                "message": "Gig updated successfully",
                "gig": gigs_db[index]
            }

    raise HTTPException(status_code=404, detail="Gig not found")
@app.delete("/gigs/{gig_id}")
def delete_gig(gig_id: int):
    """
    Delete a gig.
    """

    for index, gig in enumerate(gigs_db):

        if gig["id"] == gig_id:

            deleted_gig = gigs_db.pop(index)

            return {
                "message": "Gig deleted successfully",
                "gig": deleted_gig
            }

    raise HTTPException(status_code=404, detail="Gig not found")
