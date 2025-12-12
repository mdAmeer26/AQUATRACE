"""
Water Body Detection and Analysis Routes
Provides endpoints for detecting all water sources and analyzing their composition
"""

from fastapi import APIRouter
from typing import Optional

router = APIRouter(prefix="/water-bodies", tags=["water-bodies"])


@router.get("/detect")
async def detect_water_bodies(
    lat: float,
    lon: float,
    radius_km: float = 50
):
    """
    Detect all water bodies within a radius
    
    Args:
        lat: Latitude
        lon: Longitude
        radius_km: Search radius in kilometers
    
    Returns:
        List of detected water bodies with types
    """
    # Demo detection data
    water_bodies = [
        {
            "id": "wb_001",
            "name": "Pacific Ocean",
            "type": "ocean",
            "lat": lat,
            "lon": lon,
            "area_km2": 165200000,
            "depth_avg_m": 4000,
            "detected": True
        },
        {
            "id": "wb_002",
            "name": "Local River System",
            "type": "river",
            "lat": lat + 0.1,
            "lon": lon + 0.1,
            "length_km": 250,
            "width_avg_m": 45,
            "flow_rate_m3s": 180,
            "detected": True
        },
        {
            "id": "wb_003",
            "name": "Reservoir Dam",
            "type": "dam",
            "lat": lat - 0.05,
            "lon": lon - 0.05,
            "capacity_m3": 50000000,
            "surface_area_km2": 15,
            "detected": True
        },
        {
            "id": "wb_004",
            "name": "Natural Pond",
            "type": "pond",
            "lat": lat + 0.02,
            "lon": lon - 0.02,
            "area_m2": 8500,
            "depth_avg_m": 3,
            "detected": True
        },
        {
            "id": "wb_005",
            "name": "Coastal Bay",
            "type": "sea",
            "lat": lat - 0.08,
            "lon": lon + 0.08,
            "area_km2": 450,
            "depth_max_m": 85,
            "detected": True
        },
        {
            "id": "wb_006",
            "name": "Mountain Stream",
            "type": "river",
            "lat": lat + 0.15,
            "lon": lon - 0.12,
            "length_km": 45,
            "width_avg_m": 8,
            "flow_rate_m3s": 12,
            "detected": True
        }
    ]
    
    return {
        "location": {"lat": lat, "lon": lon},
        "radius_km": radius_km,
        "total_detected": len(water_bodies),
        "water_bodies": water_bodies,
        "types_found": {
            "ocean": 1,
            "sea": 1,
            "river": 2,
            "dam": 1,
            "pond": 1
        }
    }


@router.get("/{water_body_id}/analysis")
async def analyze_water_body(water_body_id: str):
    """
    Analyze water body composition and pollution levels
    
    Args:
        water_body_id: Water body identifier
    
    Returns:
        Detailed composition analysis and cleanup recommendations
    """
    # Comprehensive analyses for different water body types
    analyses = {
        "wb_001": _get_ocean_analysis(),
        "wb_002": _get_river_analysis(),
        "wb_003": _get_dam_analysis(),
        "wb_004": _get_pond_analysis(),
        "wb_005": _get_sea_analysis(),
        "wb_006": _get_stream_analysis()
    }
    
    return analyses.get(water_body_id, analyses["wb_001"])


def _get_ocean_analysis():
    return {
        "water_body_id": "wb_001",
        "type": "ocean",
        "name": "Pacific Ocean",
        "photos": [
            {
                "id": "photo_001",
                "url": "https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=800",
                "title": "Great Pacific Garbage Patch - Plastic Accumulation",
                "description": "Massive concentration of plastic debris floating in the North Pacific",
                "credit": "Unsplash",
                "date_taken": "2024-08-15"
            },
            {
                "id": "photo_002",
                "url": "https://images.unsplash.com/photo-1621451537084-482c73073a0f?w=800",
                "title": "Ocean Plastic Pollution",
                "description": "Close-up view of microplastics and debris in ocean waters",
                "credit": "Unsplash",
                "date_taken": "2024-09-22"
            },
            {
                "id": "photo_003",
                "url": "https://images.unsplash.com/photo-1618477461853-cf6ed80faba5?w=800",
                "title": "Marine Wildlife Impact",
                "description": "Sea turtle swimming through plastic-polluted waters",
                "credit": "Unsplash",
                "date_taken": "2024-07-10"
            },
            {
                "id": "photo_004",
                "url": "https://images.unsplash.com/photo-1591608516485-c0449fe2f250?w=800",
                "title": "Cleanup Operations",
                "description": "Ocean cleanup vessel collecting plastic debris",
                "credit": "Unsplash",
                "date_taken": "2024-10-05"
            }
        ],
        "composition_percentages": {
            "microplastics": 35.2,
            "macroplastics": 18.5,
            "organic_matter_living": 8.1,
            "organic_matter_dead": 4.2,
            "chemical_pollutants": 15.8,
            "sediment_dust": 10.2,
            "other_debris": 8.0
        },
        "plastic_types": {
            "polyethylene_PE": 45.0,
            "polypropylene_PP": 28.0,
            "polystyrene_PS": 18.0,
            "polyvinyl_chloride_PVC": 9.0
        },
        "living_organisms": {
            "affected_species": ["sea_turtles", "whales", "dolphins", "fish", "seabirds"],
            "biodiversity_impact": "severe",
            "mortality_rate": "high",
            "affected_population_percentage": 78
        },
        "non_living_debris": {
            "bottles": 35,
            "bags": 28,
            "fishing_nets": 20,
            "containers": 12,
            "other": 5
        },
        "cleanup_strategy": {
            "priority_level": "CRITICAL",
            "estimated_total_cost_usd": 2500000,
            "estimated_duration_months": 18,
            "methods": [
                {
                    "step": 1,
                    "name": "Community-Based Beach Cleanup",
                    "description": "Organize volunteer groups for coastal debris collection",
                    "materials": [
                        "Hand tools and collection bags",
                        "Basic sorting containers",
                        "Safety equipment for volunteers",
                        "Simple collection carts",
                        "Recycling bins"
                    ],
                    "equipment_cost_usd": 50000,
                    "operation_cost_usd": 100000,
                    "duration_months": 12,
                    "effectiveness_percentage": 70,
                    "coverage_area_km2": 200
                },
                {
                    "step": 2,
                    "name": "Low-Cost Floating Barriers",
                    "description": "Install simple boom systems using recycled materials",
                    "materials": [
                        "Recycled plastic pipe booms",
                        "Rope and netting",
                        "Concrete block anchors",
                        "Used barrel floats",
                        "Manual collection nets"
                    ],
                    "equipment_cost_usd": 200000,
                    "operation_cost_usd": 150000,
                    "duration_months": 12,
                    "effectiveness_percentage": 65,
                    "coverage_area_km2": 500
                },
                {
                    "step": 3,
                    "name": "Small Boat Collection Teams",
                    "description": "Use local fishing boats for debris collection",
                    "materials": [
                        "Rented fishing boats (3 vessels)",
                        "Basic nets and rakes",
                        "Fuel for boats",
                        "Storage bags",
                        "GPS devices"
                    ],
                    "equipment_cost_usd": 150000,
                    "operation_cost_usd": 200000,
                    "duration_months": 18,
                    "effectiveness_percentage": 60,
                    "target_particle_size_microns": 5000
                },
                {
                    "step": 4,
                    "name": "Educational Awareness Program",
                    "description": "Prevent future pollution through education",
                    "materials": [
                        "Educational posters and banners",
                        "Community workshops",
                        "Social media campaigns",
                        "School programs",
                        "Signage at beaches"
                    ],
                    "equipment_cost_usd": 80000,
                    "operation_cost_usd": 70000,
                    "duration_months": 12,
                    "effectiveness_percentage": 80,
                    "biodegradation_rate": "prevention"
                }
            ],
            "prevention_measures": [
                "Implement coastal waste management infrastructure",
                "Ban single-use plastics in coastal regions",
                "Install river mouth barrier systems",
                "International shipping waste regulations",
                "Public awareness campaigns",
                "Plastic alternatives research funding"
            ],
            "ongoing_maintenance": {
                "frequency": "continuous",
                "annual_cost_usd": 8000000,
                "required_personnel": 150
            }
        }
    }


def _get_river_analysis():
    return {
        "water_body_id": "wb_002",
        "type": "river",
        "name": "Local River System",
        "photos": [
            {
                "id": "photo_r001",
                "url": "https://images.unsplash.com/photo-1611273426858-450d8e3c9fce?w=800",
                "title": "River Plastic Pollution",
                "description": "Plastic bottles and bags accumulating along riverbank",
                "credit": "Unsplash",
                "date_taken": "2024-09-18"
            },
            {
                "id": "photo_r002",
                "url": "https://images.unsplash.com/photo-1583909492116-b1b916f0d45c?w=800",
                "title": "River Boom Barrier",
                "description": "Floating barrier system catching debris in river",
                "credit": "Unsplash",
                "date_taken": "2024-08-25"
            },
            {
                "id": "photo_r003",
                "url": "https://images.unsplash.com/photo-1605289355680-75fb41239154?w=800",
                "title": "Polluted Riverbank",
                "description": "Various plastic debris scattered along river shore",
                "credit": "Unsplash",
                "date_taken": "2024-10-12"
            },
            {
                "id": "photo_r004",
                "url": "https://images.unsplash.com/photo-1530587191325-3db32d826c18?w=800",
                "title": "River Cleanup Volunteers",
                "description": "Community cleanup operation removing waste from river",
                "credit": "Unsplash",
                "date_taken": "2024-11-03"
            }
        ],
        "composition_percentages": {
            "microplastics": 22.5,
            "macroplastics": 28.3,
            "organic_matter_living": 12.5,
            "organic_matter_dead": 6.2,
            "chemical_pollutants": 12.4,
            "sediment_dust": 14.8,
            "other_debris": 3.3
        },
        "plastic_types": {
            "polyethylene_PE": 38.0,
            "polypropylene_PP": 32.0,
            "polystyrene_PS": 20.0,
            "polyvinyl_chloride_PVC": 10.0
        },
        "living_organisms": {
            "affected_species": ["fish", "amphibians", "aquatic_insects", "freshwater_plants", "turtles"],
            "biodiversity_impact": "moderate",
            "mortality_rate": "medium",
            "affected_population_percentage": 52
        },
        "non_living_debris": {
            "bottles": 32,
            "bags": 25,
            "food_wrappers": 18,
            "straws": 15,
            "cans": 10
        },
        "cleanup_strategy": {
            "priority_level": "HIGH",
            "estimated_total_cost_usd": 180000,
            "estimated_duration_months": 8,
            "methods": [
                {
                    "step": 1,
                    "name": "DIY River Boom Barriers",
                    "description": "Build low-cost barriers using local materials",
                    "materials": [
                        "Bamboo or PVC pipes (200m)",
                        "Rope and used fishing nets",
                        "Concrete blocks for anchors",
                        "Wooden collection platforms",
                        "Basic tools"
                    ],
                    "equipment_cost_usd": 15000,
                    "operation_cost_usd": 10000,
                    "duration_months": 2,
                    "effectiveness_percentage": 75,
                    "debris_captured_daily_kg": 150
                },
                {
                    "step": 2,
                    "name": "Volunteer Manual Cleanup",
                    "description": "Organized community river cleanup drives",
                    "materials": [
                        "Hand tools and rakes",
                        "Collection bags and gloves",
                        "Waders for volunteers",
                        "Basic sorting bins",
                        "Refreshments for volunteers"
                    ],
                    "equipment_cost_usd": 8000,
                    "operation_cost_usd": 12000,
                    "duration_months": 6,
                    "effectiveness_percentage": 70,
                    "debris_removed_tons": 120
                },
                {
                    "step": 3,
                    "name": "Native Plant Restoration",
                    "description": "Plant local vegetation for natural filtration",
                    "materials": [
                        "Native plant saplings (2,000 units)",
                        "Mulch and compost",
                        "Simple erosion barriers",
                        "Community planting tools",
                        "Rainwater for irrigation"
                    ],
                    "equipment_cost_usd": 18000,
                    "operation_cost_usd": 15000,
                    "duration_months": 8,
                    "effectiveness_percentage": 65,
                    "restoration_area_hectares": 8
                },
                {
                    "step": 4,
                    "name": "Simple Filtration System",
                    "description": "Basic gravel and sand biofilters",
                    "materials": [
                        "Gravel and sand beds",
                        "Simple aeration pipes",
                        "Natural settling areas",
                        "Manual monitoring tools",
                        "Water testing kits"
                    ],
                    "equipment_cost_usd": 50000,
                    "operation_cost_usd": 52000,
                    "duration_months": 4,
                    "effectiveness_percentage": 60,
                    "treatment_capacity_m3_day": 15000
                }
            ],
            "prevention_measures": [
                "Weekly monitoring and maintenance",
                "Upstream waste interception points",
                "Community cleanup programs (monthly)",
                "Stormwater management upgrades",
                "Littering fines enforcement",
                "Recycling education programs"
            ],
            "ongoing_maintenance": {
                "frequency": "weekly",
                "annual_cost_usd": 120000,
                "required_personnel": 8
            }
        }
    }


def _get_dam_analysis():
    return {
        "water_body_id": "wb_003",
        "type": "dam",
        "name": "Reservoir Dam",
        "photos": [
            {
                "id": "photo_d001",
                "url": "https://images.unsplash.com/photo-1547638375-49c0ed8c41b4?w=800",
                "title": "Reservoir Dam Overview",
                "description": "Aerial view of reservoir with visible surface debris",
                "credit": "Unsplash",
                "date_taken": "2024-08-30"
            },
            {
                "id": "photo_d002",
                "url": "https://images.unsplash.com/photo-1566933293069-b55c7f326d8c?w=800",
                "title": "Dam Sediment Buildup",
                "description": "Sediment and debris accumulation at dam intake",
                "credit": "Unsplash",
                "date_taken": "2024-09-14"
            },
            {
                "id": "photo_d003",
                "url": "https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=800",
                "title": "Floating Debris",
                "description": "Plastic containers and fishing gear on reservoir surface",
                "credit": "Unsplash",
                "date_taken": "2024-10-20"
            },
            {
                "id": "photo_d004",
                "url": "https://images.unsplash.com/photo-1501594907352-04cda38ebc29?w=800",
                "title": "Dredging Operations",
                "description": "Mechanical dredging removing accumulated sediment",
                "credit": "Unsplash",
                "date_taken": "2024-11-08"
            }
        ],
        "composition_percentages": {
            "microplastics": 15.8,
            "macroplastics": 12.5,
            "organic_matter_living": 16.8,
            "organic_matter_dead": 8.5,
            "chemical_pollutants": 8.2,
            "sediment_dust": 32.7,
            "other_debris": 5.5
        },
        "plastic_types": {
            "polyethylene_PE": 42.0,
            "polypropylene_PP": 30.0,
            "polystyrene_PS": 18.0,
            "polyvinyl_chloride_PVC": 10.0
        },
        "living_organisms": {
            "affected_species": ["fish", "waterfowl", "zooplankton", "algae"],
            "biodiversity_impact": "moderate",
            "mortality_rate": "low_to_medium",
            "affected_population_percentage": 38
        },
        "non_living_debris": {
            "bottles": 30,
            "fishing_gear": 25,
            "logs_branches": 20,
            "construction_material": 15,
            "other": 10
        },
        "cleanup_strategy": {
            "priority_level": "MEDIUM",
            "estimated_total_cost_usd": 145000,
            "estimated_duration_months": 10,
            "methods": [
                {
                    "step": 1,
                    "name": "Manual Surface Skimming",
                    "description": "Use small boats for floating debris collection",
                    "materials": [
                        "Rented small boats (2 units)",
                        "Hand-held nets and rakes",
                        "Floating collection baskets",
                        "Storage containers",
                        "Basic safety gear"
                    ],
                    "equipment_cost_usd": 12000,
                    "operation_cost_usd": 18000,
                    "duration_months": 4,
                    "effectiveness_percentage": 70,
                    "debris_collected_daily_kg": 80
                },
                {
                    "step": 2,
                    "name": "Targeted Sediment Removal",
                    "description": "Focus on critical areas only using manual methods",
                    "materials": [
                        "Rented excavator (1 unit)",
                        "Manual shovels and rakes",
                        "Simple pump system",
                        "Dump truck rental",
                        "Basic disposal site"
                    ],
                    "equipment_cost_usd": 35000,
                    "operation_cost_usd": 28000,
                    "duration_months": 6,
                    "effectiveness_percentage": 60,
                    "sediment_removed_m3": 8000
                },
                {
                    "step": 3,
                    "name": "DIY Intake Screening",
                    "description": "Install basic mesh screens at intake points",
                    "materials": [
                        "Wire mesh screens (5mm)",
                        "Manual cleaning tools",
                        "Simple frame structures",
                        "Regular cleaning schedule",
                        "Basic monitoring"
                    ],
                    "equipment_cost_usd": 8000,
                    "operation_cost_usd": 7000,
                    "duration_months": 1,
                    "effectiveness_percentage": 65,
                    "filtration_capacity_m3_hr": 2000
                },
                {
                    "step": 4,
                    "name": "Natural Algae Control",
                    "description": "Use natural methods to control algae growth",
                    "materials": [
                        "Barley straw bales",
                        "Natural bacteria treatments",
                        "Simple aeration (windmill)",
                        "Manual removal",
                        "Water testing kits"
                    ],
                    "equipment_cost_usd": 15000,
                    "operation_cost_usd": 22000,
                    "duration_months": 10,
                    "effectiveness_percentage": 55,
                    "treatment_coverage_hectares": 60
                }
            ],
            "prevention_measures": [
                "Upstream watershed protection zones",
                "Bi-weekly maintenance inspections",
                "Continuous water quality monitoring",
                "Access control for recreation",
                "Nutrient runoff reduction",
                "Emergency spillway debris gates"
            ],
            "ongoing_maintenance": {
                "frequency": "bi-weekly",
                "annual_cost_usd": 85000,
                "required_personnel": 6
            }
        }
    }


def _get_pond_analysis():
    return {
        "water_body_id": "wb_004",
        "type": "pond",
        "name": "Natural Pond",
        "photos": [
            {
                "id": "photo_p001",
                "url": "https://images.unsplash.com/photo-1439920120577-eb3a83c16dd7?w=800",
                "title": "Peaceful Pond Scene",
                "description": "Small natural pond surrounded by vegetation",
                "credit": "Unsplash",
                "date_taken": "2024-07-22"
            },
            {
                "id": "photo_p002",
                "url": "https://images.unsplash.com/photo-1582967788606-a171c1080cb0?w=800",
                "title": "Pond Litter Problem",
                "description": "Plastic bags and bottles floating in pond water",
                "credit": "Unsplash",
                "date_taken": "2024-08-16"
            },
            {
                "id": "photo_p003",
                "url": "https://images.unsplash.com/photo-1535083783855-76ae62b2914e?w=800",
                "title": "Volunteer Cleanup",
                "description": "Community members cleaning pond with nets and tools",
                "credit": "Unsplash",
                "date_taken": "2024-09-28"
            },
            {
                "id": "photo_p004",
                "url": "https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=800",
                "title": "Restored Pond",
                "description": "Pond after cleanup with healthy aquatic plants",
                "credit": "Unsplash",
                "date_taken": "2024-11-15"
            }
        ],
        "composition_percentages": {
            "microplastics": 8.2,
            "macroplastics": 6.5,
            "organic_matter_living": 32.4,
            "organic_matter_dead": 13.4,
            "chemical_pollutants": 4.3,
            "sediment_dust": 28.7,
            "other_debris": 6.5
        },
        "plastic_types": {
            "polyethylene_PE": 40.0,
            "polypropylene_PP": 35.0,
            "polystyrene_PS": 15.0,
            "polyvinyl_chloride_PVC": 10.0
        },
        "living_organisms": {
            "affected_species": ["frogs", "fish", "dragonflies", "aquatic_plants", "snails"],
            "biodiversity_impact": "low_to_moderate",
            "mortality_rate": "low",
            "affected_population_percentage": 22
        },
        "non_living_debris": {
            "bags": 35,
            "bottles": 30,
            "food_wrappers": 20,
            "straws_cups": 10,
            "other": 5
        },
        "cleanup_strategy": {
            "priority_level": "LOW_TO_MEDIUM",
            "estimated_total_cost_usd": 5800,
            "estimated_duration_months": 4,
            "methods": [
                {
                    "step": 1,
                    "name": "Community Cleanup Drive",
                    "description": "Free volunteer-based debris collection",
                    "materials": [
                        "Borrowed nets and rakes",
                        "Reused plastic bags",
                        "Community volunteers",
                        "Basic gloves",
                        "Homemade tools"
                    ],
                    "equipment_cost_usd": 500,
                    "operation_cost_usd": 800,
                    "duration_months": 1,
                    "effectiveness_percentage": 90,
                    "volunteer_hours": 80
                },
                {
                    "step": 2,
                    "name": "Free Natural Plants",
                    "description": "Plant native species collected from nearby areas",
                    "materials": [
                        "Free native plants from nature",
                        "Local gravel for biofilter",
                        "Donated wetland plants",
                        "Recycled containers",
                        "Natural mulch"
                    ],
                    "equipment_cost_usd": 800,
                    "operation_cost_usd": 600,
                    "duration_months": 2,
                    "effectiveness_percentage": 65,
                    "filtration_area_m2": 80
                },
                {
                    "step": 3,
                    "name": "DIY Wind-Powered Aeration",
                    "description": "Build simple windmill aerator using scrap materials",
                    "materials": [
                        "Recycled materials for windmill",
                        "PVC pipe diffusers",
                        "Used bicycle parts",
                        "Rope and pulleys",
                        "Scrap metal frame"
                    ],
                    "equipment_cost_usd": 600,
                    "operation_cost_usd": 400,
                    "duration_months": 1,
                    "effectiveness_percentage": 50,
                    "oxygen_increase_percentage": 30
                },
                {
                    "step": 4,
                    "name": "Natural Bacteria Treatment",
                    "description": "Use compost tea and natural enzymes",
                    "materials": [
                        "Homemade compost tea",
                        "Natural enzymes (papaya, pineapple)",
                        "Beneficial soil bacteria",
                        "DIY pH test strips",
                        "Natural clarifiers"
                    ],
                    "equipment_cost_usd": 400,
                    "operation_cost_usd": 700,
                    "duration_months": 4,
                    "effectiveness_percentage": 50,
                    "treatment_frequency": "bi-weekly"
                }
            ],
            "prevention_measures": [
                "Install trash barriers at inlets",
                "Community education signage",
                "Monthly volunteer cleanup days",
                "Native plant buffer zones",
                "Wildlife-friendly fencing",
                "No-littering enforcement"
            ],
            "ongoing_maintenance": {
                "frequency": "monthly",
                "annual_cost_usd": 3000,
                "required_personnel": 2
            }
        }
    }


def _get_sea_analysis():
    return {
        "water_body_id": "wb_005",
        "type": "sea",
        "name": "Coastal Bay",
        "photos": [
            {
                "id": "photo_s001",
                "url": "https://images.unsplash.com/photo-1583909492116-b1b916f0d45c?w=800",
                "title": "Coastal Bay Pollution",
                "description": "Plastic debris washing up on bay shoreline",
                "credit": "Unsplash",
                "date_taken": "2024-08-08"
            },
            {
                "id": "photo_s002",
                "url": "https://images.unsplash.com/photo-1621451537084-482c73073a0f?w=800",
                "title": "Beach Littered with Plastic",
                "description": "Various plastic items scattered across coastal beach",
                "credit": "Unsplash",
                "date_taken": "2024-09-05"
            },
            {
                "id": "photo_s003",
                "url": "https://images.unsplash.com/photo-1591608516485-c0449fe2f250?w=800",
                "title": "Marine Cleanup Vessel",
                "description": "Boat collecting floating debris from bay waters",
                "credit": "Unsplash",
                "date_taken": "2024-10-18"
            },
            {
                "id": "photo_s004",
                "url": "https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=800",
                "title": "Underwater Debris",
                "description": "Divers removing fishing nets and plastic from seabed",
                "credit": "Unsplash",
                "date_taken": "2024-11-22"
            }
        ],
        "composition_percentages": {
            "microplastics": 28.5,
            "macroplastics": 22.3,
            "organic_matter_living": 10.2,
            "organic_matter_dead": 5.5,
            "chemical_pollutants": 13.8,
            "sediment_dust": 12.5,
            "other_debris": 7.2
        },
        "plastic_types": {
            "polyethylene_PE": 43.0,
            "polypropylene_PP": 29.0,
            "polystyrene_PS": 19.0,
            "polyvinyl_chloride_PVC": 9.0
        },
        "living_organisms": {
            "affected_species": ["fish", "crustaceans", "mollusks", "seabirds", "coral", "marine_plants"],
            "biodiversity_impact": "high",
            "mortality_rate": "medium_to_high",
            "affected_population_percentage": 64
        },
        "non_living_debris": {
            "bottles": 28,
            "bags": 24,
            "fishing_gear": 22,
            "buoys_floats": 15,
            "other": 11
        },
        "cleanup_strategy": {
            "priority_level": "HIGH",
            "estimated_total_cost_usd": 220000,
            "estimated_duration_months": 10,
            "methods": [
                {
                    "step": 1,
                    "name": "Beach Cleanup Volunteers",
                    "description": "Organize regular community beach cleanup events",
                    "materials": [
                        "Hand rakes and bags",
                        "Borrowed pickup trucks",
                        "Simple hand tools",
                        "Volunteer coordination",
                        "Free labor from community"
                    ],
                    "equipment_cost_usd": 15000,
                    "operation_cost_usd": 20000,
                    "duration_months": 6,
                    "effectiveness_percentage": 75,
                    "coastline_coverage_km": 25
                },
                {
                    "step": 2,
                    "name": "Low-Cost Floating Nets",
                    "description": "Simple net barriers using recycled materials",
                    "materials": [
                        "Recycled fishing nets (500m)",
                        "Wooden collection frames",
                        "Rented small boats (2)",
                        "Rope and barrel anchors",
                        "Manual collection"
                    ],
                    "equipment_cost_usd": 40000,
                    "operation_cost_usd": 35000,
                    "duration_months": 10,
                    "effectiveness_percentage": 65,
                    "debris_intercepted_daily_kg": 120
                },
                {
                    "step": 3,
                    "name": "Snorkeling Cleanup Teams",
                    "description": "Shallow water debris removal by volunteers",
                    "materials": [
                        "Basic snorkel gear (10 sets)",
                        "Collection bags",
                        "Volunteer divers",
                        "Simple GPS markers",
                        "Borrowed kayaks for support"
                    ],
                    "equipment_cost_usd": 18000,
                    "operation_cost_usd": 22000,
                    "duration_months": 6,
                    "effectiveness_percentage": 55,
                    "dive_sites": 15
                },
                {
                    "step": 4,
                    "name": "Simple Marina Stations",
                    "description": "Basic waste bins and education at harbors",
                    "materials": [
                        "Simple waste bins (8 units)",
                        "DIY recycling stations",
                        "Printed educational posters",
                        "Volunteer monitoring",
                        "Basic signage"
                    ],
                    "equipment_cost_usd": 28000,
                    "operation_cost_usd": 42000,
                    "duration_months": 4,
                    "effectiveness_percentage": 70,
                    "marinas_upgraded": 4
                }
            ],
            "prevention_measures": [
                "Regulate coastal development",
                "Install stormwater filtration systems",
                "Beach access management",
                "Fishing gear buyback program",
                "Ban single-use plastics at beaches",
                "Tourist education campaigns"
            ],
            "ongoing_maintenance": {
                "frequency": "daily",
                "annual_cost_usd": 180000,
                "required_personnel": 15
            }
        }
    }


def _get_stream_analysis():
    return {
        "water_body_id": "wb_006",
        "type": "river",
        "name": "Mountain Stream",
        "photos": [
            {
                "id": "photo_st001",
                "url": "https://images.unsplash.com/photo-1501594907352-04cda38ebc29?w=800",
                "title": "Pristine Mountain Stream",
                "description": "Clear stream flowing through mountain forest",
                "credit": "Unsplash",
                "date_taken": "2024-07-05"
            },
            {
                "id": "photo_st002",
                "url": "https://images.unsplash.com/photo-1611273426858-450d8e3c9fce?w=800",
                "title": "Trail Litter Impact",
                "description": "Plastic bottles and wrappers left by hikers near stream",
                "credit": "Unsplash",
                "date_taken": "2024-08-20"
            },
            {
                "id": "photo_st003",
                "url": "https://images.unsplash.com/photo-1530587191325-3db32d826c18?w=800",
                "title": "Stream Restoration",
                "description": "Volunteers stabilizing streambank with native plants",
                "credit": "Unsplash",
                "date_taken": "2024-09-30"
            },
            {
                "id": "photo_st004",
                "url": "https://images.unsplash.com/photo-1439920120577-eb3a83c16dd7?w=800",
                "title": "Healthy Stream Ecosystem",
                "description": "Stream after cleanup showing clear water and wildlife",
                "credit": "Unsplash",
                "date_taken": "2024-11-12"
            }
        ],
        "composition_percentages": {
            "microplastics": 5.2,
            "macroplastics": 8.5,
            "organic_matter_living": 22.3,
            "organic_matter_dead": 18.7,
            "chemical_pollutants": 3.2,
            "sediment_dust": 38.6,
            "other_debris": 3.5
        },
        "plastic_types": {
            "polyethylene_PE": 35.0,
            "polypropylene_PP": 30.0,
            "polystyrene_PS": 25.0,
            "polyvinyl_chloride_PVC": 10.0
        },
        "living_organisms": {
            "affected_species": ["trout", "salamanders", "mayflies", "stream_plants"],
            "biodiversity_impact": "low",
            "mortality_rate": "low",
            "affected_population_percentage": 15
        },
        "non_living_debris": {
            "bottles": 40,
            "wrappers": 25,
            "cans": 20,
            "bags": 10,
            "other": 5
        },
        "cleanup_strategy": {
            "priority_level": "MEDIUM",
            "estimated_total_cost_usd": 32000,
            "estimated_duration_months": 6,
            "methods": [
                {
                    "step": 1,
                    "name": "Hiker Cleanup Initiative",
                    "description": "Engage hikers to pack out trash they find",
                    "materials": [
                        "Donated trash bags at trailheads",
                        "Free collection buckets",
                        "Homemade signage",
                        "Trail markers from stones",
                        "Volunteer coordination"
                    ],
                    "equipment_cost_usd": 3000,
                    "operation_cost_usd": 4000,
                    "duration_months": 3,
                    "effectiveness_percentage": 80,
                    "trail_length_km": 15
                },
                {
                    "step": 2,
                    "name": "Natural Erosion Control",
                    "description": "Use free natural materials for stabilization",
                    "materials": [
                        "Free native plants from wild",
                        "Rocks collected from site",
                        "Natural logs and branches",
                        "Volunteer labor",
                        "Donated mulch"
                    ],
                    "equipment_cost_usd": 6000,
                    "operation_cost_usd": 5000,
                    "duration_months": 5,
                    "effectiveness_percentage": 65,
                    "restoration_length_km": 4
                },
                {
                    "step": 3,
                    "name": "Student Monitoring Teams",
                    "description": "Partner with schools for free monitoring",
                    "materials": [
                        "Basic DIY water test kits",
                        "Free smartphone apps for data",
                        "Borrowed safety equipment",
                        "Student volunteers",
                        "Digital training materials"
                    ],
                    "equipment_cost_usd": 6000,
                    "operation_cost_usd": 8000,
                    "duration_months": 6,
                    "effectiveness_percentage": 60,
                    "volunteer_teams": 3
                }
            ],
            "prevention_measures": [
                "Install debris traps at trail heads",
                "Leave No Trace education",
                "Seasonal monitoring",
                "Recreation impact management",
                "Pack-in pack-out policies"
            ],
            "ongoing_maintenance": {
                "frequency": "monthly",
                "annual_cost_usd": 25000,
                "required_personnel": 3
            }
        }
    }
