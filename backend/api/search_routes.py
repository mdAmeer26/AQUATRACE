"""
Location-based Water Source Search Routes
Provides search functionality for water bodies by location name
"""

from fastapi import APIRouter
from typing import Optional, List

router = APIRouter(prefix="/search", tags=["search"])


# Comprehensive Indian Water Sources Database
INDIAN_RIVERS = [
    "Ganga", "Yamuna", "Saraswati", "Ghaghara", "Gandak", "Kosi", "Sone", "Chambal", "Betwa", "Ken", "Tons", "Ramganga", "Sharda", "Gomti", "Sarayu", "Rapti", "Mahananda", "Damodar", "Hooghly", "Teesta", "Brahmaputra", "Subansiri", "Manas", "Torsha", "Sankosh", "Dibang", "Lohit", "Kameng", "Barak", "Surma", "Jhelum", "Chenab", "Ravi", "Beas", "Sutlej", "Indus", "Nubra", "Shyok", "Zanskar", "Spiti", "Parvati", "Baspa", "Markha", "Lidder", "Tawi", "Ujh", "Krishna", "Tungabhadra", "Bhima", "Musi", "Koyna", "Panchganga", "Ghataprabha", "Malaprabha", "Godavari", "Pravara", "Purna", "Sabari", "Vamsadhara", "Nagavali", "Penna", "Palar", "Cauvery", "Hemavati", "Arkavathi", "Amaravathi", "Bhavani", "Noyyal", "Kabini", "Shimsha", "Luni", "Sabarmati", "Mahi", "Tapi", "Narmada", "Mahanadi", "Tel", "Brahmani", "Baitarani", "Subarnarekha", "Rushikulya", "Periyar", "Bharathapuzha", "Pamba", "Vaigai", "Thamirabarani", "Sharavathi", "Netravati", "Mandovi", "Zuari"
]

INDIAN_LAKES = [
    "Wular Lake", "Dal Lake", "Pangong Tso", "Tso Moriri", "Chilika Lake", "Vembanad Lake", "Loktak Lake", "Bhojtal", "Sambhar Lake", "Pulicat Lake", "Kolleru Lake", "Lonar Lake", "Nainital Lake", "Bhimtal", "Sattal", "Naukuchiatal", "Tsomgo Lake", "Gurudongmar Lake", "Umiam Lake", "Ashtamudi Lake", "Sasthamkotta Lake", "Ooty Lake", "Kodaikanal Lake", "Pichola Lake", "Fateh Sagar Lake", "Pushkar Lake", "Ana Sagar Lake", "Nakki Lake", "Kankaria Lake", "Sukhna Lake", "Ulsoor Lake", "Hebbal Lake", "Bellandur Lake", "Powai Lake", "Hussain Sagar Lake", "Venna Lake", "Pawna Lake"
]

INDIAN_RESERVOIRS = [
    "Gobind Sagar", "Tehri Dam", "Hirakud Reservoir", "Nagarjuna Sagar", "Indira Sagar", "Sardar Sarovar", "Rihand Reservoir", "Bhakra Dam", "Srisailam Reservoir", "Mettur Dam", "Koyna Dam", "Idukki Dam", "Tungabhadra Dam", "Almatti Dam", "Gandhi Sagar", "Ukai Dam", "Krishnaraja Sagar", "Bhadra Reservoir", "Ranjit Sagar", "Pong Dam"
]

# Generate coordinates for Indian water sources (simplified - using approximate locations)
def generate_indian_water_sources():
    """Generate comprehensive Indian water sources with coordinates"""
    sources = []
    
    # Major Rivers
    river_locations = {
        "Ganga": (25.3, 83.0), "Yamuna": (25.5, 81.8), "Brahmaputra": (26.0, 91.0),
        "Godavari": (18.7, 77.5), "Krishna": (16.5, 76.5), "Narmada": (22.5, 77.0),
        "Cauvery": (12.4, 77.8), "Mahanadi": (20.5, 84.0), "Tapi": (21.0, 73.5),
        "Sutlej": (31.0, 75.5), "Beas": (31.5, 75.8), "Chenab": (33.0, 74.5),
        "Jhelum": (34.5, 74.8), "Ravi": (32.5, 75.0), "Indus": (34.0, 74.0),
        "Periyar": (9.9, 76.5), "Sabarmati": (23.0, 72.6), "Luni": (26.0, 73.0),
        "Damodar": (23.5, 87.0), "Brahmani": (21.0, 85.5), "Mahi": (23.5, 73.5),
        "Betwa": (25.5, 78.5), "Chambal": (26.0, 79.0), "Kosi": (26.5, 87.0),
        "Musi": (17.3, 78.5), "Bhima": (17.5, 75.5), "Tungabhadra": (15.3, 76.5)
    }
    
    # Generate river data
    for river in INDIAN_RIVERS[:30]:  # First 30 major rivers
        lat, lon = river_locations.get(river, (20.5, 78.5))
        sources.append({
            "id": f"in_river_{river.lower().replace(' ', '_')}",
            "name": f"{river} River",
            "type": "river",
            "location": f"India",
            "lat": lat,
            "lon": lon,
            "contamination_level": ["low", "medium", "high"][hash(river) % 3],
            "detected_contaminants": ["agricultural_runoff", "industrial_waste", "plastic", "sewage"][:(hash(river) % 4) + 1],
            "water_quality_index": 40 + (hash(river) % 40)
        })
    
    # Major Lakes
    lake_locations = {
        "Wular Lake": (34.4, 74.6), "Dal Lake": (34.1, 74.8), "Chilika Lake": (19.7, 85.3),
        "Vembanad Lake": (9.6, 76.4), "Loktak Lake": (24.5, 93.8), "Sambhar Lake": (26.9, 75.2),
        "Pulicat Lake": (13.6, 80.3), "Kolleru Lake": (16.7, 81.3), "Bhojtal": (23.2, 77.4),
        "Pangong Tso": (33.7, 78.7), "Tso Moriri": (32.9, 78.3), "Nainital Lake": (29.4, 79.5),
        "Pichola Lake": (24.6, 73.7), "Fateh Sagar Lake": (24.6, 73.7), "Hussain Sagar": (17.4, 78.5)
    }
    
    for lake in INDIAN_LAKES[:20]:  # First 20 major lakes
        lat, lon = lake_locations.get(lake, (20.5, 78.5))
        sources.append({
            "id": f"in_lake_{lake.lower().replace(' ', '_')}",
            "name": lake,
            "type": "lake",
            "location": f"India",
            "lat": lat,
            "lon": lon,
            "contamination_level": ["low", "medium"][hash(lake) % 2],
            "detected_contaminants": ["algae", "plastic", "sewage"][:(hash(lake) % 3) + 1],
            "water_quality_index": 50 + (hash(lake) % 30)
        })
    
    # Major Reservoirs/Dams
    reservoir_locations = {
        "Gobind Sagar": (31.4, 76.5), "Tehri Dam": (30.4, 78.5), "Hirakud Reservoir": (21.5, 84.0),
        "Nagarjuna Sagar": (16.6, 79.3), "Indira Sagar": (22.2, 76.5), "Sardar Sarovar": (21.8, 73.6),
        "Bhakra Dam": (31.4, 76.4), "Srisailam Reservoir": (16.1, 78.9), "Mettur Dam": (11.8, 77.8),
        "Idukki Dam": (9.8, 77.0), "Koyna Dam": (17.4, 73.8)
    }
    
    for reservoir in INDIAN_RESERVOIRS[:15]:  # First 15 major reservoirs
        lat, lon = reservoir_locations.get(reservoir, (20.5, 78.5))
        sources.append({
            "id": f"in_reservoir_{reservoir.lower().replace(' ', '_')}",
            "name": reservoir,
            "type": "reservoir",
            "location": f"India",
            "lat": lat,
            "lon": lon,
            "contamination_level": "low",
            "detected_contaminants": ["silt", "algae"],
            "water_quality_index": 60 + (hash(reservoir) % 25)
        })
    
    return sources

# Generate Indian water sources
COMPREHENSIVE_INDIAN_SOURCES = generate_indian_water_sources()

# Database of water sources by location (can be expanded)
LOCATION_WATER_SOURCES = {
    "telangana": [
        {
            "id": "tel_001",
            "name": "Hussain Sagar Lake",
            "type": "lake",
            "location": "Hyderabad, Telangana",
            "lat": 17.4239,
            "lon": 78.4738,
            "area_km2": 5.7,
            "contamination_level": "high",
            "detected_contaminants": ["sewage", "industrial_waste", "plastic", "heavy_metals"],
            "water_quality_index": 45
        },
        {
            "id": "tel_002",
            "name": "Godavari River",
            "type": "river",
            "location": "Northern Telangana",
            "lat": 18.7465,
            "lon": 79.0148,
            "length_km": 312,
            "contamination_level": "medium",
            "detected_contaminants": ["agricultural_runoff", "plastic", "organic_waste"],
            "water_quality_index": 62
        },
        {
            "id": "tel_003",
            "name": "Osman Sagar (Gandipet Lake)",
            "type": "reservoir",
            "location": "Hyderabad, Telangana",
            "lat": 17.3014,
            "lon": 78.2744,
            "capacity_m3": 46000000,
            "contamination_level": "medium",
            "detected_contaminants": ["silt", "algae", "plastic", "pesticides"],
            "water_quality_index": 58
        },
        {
            "id": "tel_004",
            "name": "Himayat Sagar",
            "type": "reservoir",
            "location": "Hyderabad, Telangana",
            "lat": 17.2645,
            "lon": 78.3089,
            "capacity_m3": 52400000,
            "contamination_level": "medium",
            "detected_contaminants": ["silt", "agricultural_runoff", "plastic"],
            "water_quality_index": 61
        },
        {
            "id": "tel_005",
            "name": "Krishna River",
            "type": "river",
            "location": "Southern Telangana",
            "lat": 16.5062,
            "lon": 80.6480,
            "length_km": 285,
            "contamination_level": "high",
            "detected_contaminants": ["industrial_waste", "sewage", "plastic", "chemicals"],
            "water_quality_index": 48
        },
        {
            "id": "tel_006",
            "name": "Musi River",
            "type": "river",
            "location": "Hyderabad, Telangana",
            "lat": 17.3850,
            "lon": 78.4867,
            "length_km": 267,
            "contamination_level": "critical",
            "detected_contaminants": ["sewage", "industrial_waste", "toxic_chemicals", "plastic", "heavy_metals"],
            "water_quality_index": 28
        },
        {
            "id": "tel_007",
            "name": "Nagarjuna Sagar Dam",
            "type": "dam",
            "location": "Nalgonda, Telangana",
            "lat": 16.5770,
            "lon": 79.3167,
            "capacity_m3": 11472000000,
            "contamination_level": "low",
            "detected_contaminants": ["silt", "algae"],
            "water_quality_index": 72
        },
        {
            "id": "tel_008",
            "name": "Durgam Cheruvu (Secret Lake)",
            "type": "lake",
            "location": "Hyderabad, Telangana",
            "lat": 17.4406,
            "lon": 78.3794,
            "area_km2": 0.63,
            "contamination_level": "medium",
            "detected_contaminants": ["sewage", "plastic", "organic_waste"],
            "water_quality_index": 55
        },
        {
            "id": "tel_009",
            "name": "Pocharam Lake",
            "type": "lake",
            "location": "Medak, Telangana",
            "lat": 17.8456,
            "lon": 78.2689,
            "area_km2": 13.0,
            "contamination_level": "low",
            "detected_contaminants": ["algae", "silt"],
            "water_quality_index": 68
        },
        {
            "id": "tel_010",
            "name": "Pakhal Lake",
            "type": "lake",
            "location": "Warangal, Telangana",
            "lat": 17.9833,
            "lon": 79.9500,
            "area_km2": 30.0,
            "contamination_level": "low",
            "detected_contaminants": ["silt", "organic_matter"],
            "water_quality_index": 70
        }
    ],
    "hyderabad": [
        {
            "id": "hyd_001",
            "name": "Hussain Sagar Lake",
            "type": "lake",
            "location": "Hyderabad",
            "lat": 17.4239,
            "lon": 78.4738,
            "area_km2": 5.7,
            "contamination_level": "high",
            "detected_contaminants": ["sewage", "industrial_waste", "plastic", "heavy_metals"],
            "water_quality_index": 45
        },
        {
            "id": "hyd_002",
            "name": "Musi River",
            "type": "river",
            "location": "Hyderabad",
            "lat": 17.3850,
            "lon": 78.4867,
            "length_km": 267,
            "contamination_level": "critical",
            "detected_contaminants": ["sewage", "industrial_waste", "toxic_chemicals", "plastic", "heavy_metals"],
            "water_quality_index": 28
        },
        {
            "id": "hyd_003",
            "name": "Durgam Cheruvu",
            "type": "lake",
            "location": "Hyderabad",
            "lat": 17.4406,
            "lon": 78.3794,
            "area_km2": 0.63,
            "contamination_level": "medium",
            "detected_contaminants": ["sewage", "plastic", "organic_waste"],
            "water_quality_index": 55
        }
    ],
    "maharashtra": [
        {
            "id": "mah_001",
            "name": "Godavari River",
            "type": "river",
            "location": "Maharashtra",
            "lat": 19.8762,
            "lon": 75.3433,
            "length_km": 900,
            "contamination_level": "medium",
            "detected_contaminants": ["industrial_waste", "agricultural_runoff", "plastic"],
            "water_quality_index": 60
        }
    ],
    "karnataka": [
        {
            "id": "kar_001",
            "name": "Krishna River",
            "type": "river",
            "location": "Karnataka",
            "lat": 16.2160,
            "lon": 74.8630,
            "length_km": 340,
            "contamination_level": "medium",
            "detected_contaminants": ["agricultural_runoff", "industrial_waste", "plastic"],
            "water_quality_index": 58
        }
    ],
    
    # NORTH AMERICA
    "usa": [
        {
            "id": "usa_001",
            "name": "Lake Michigan",
            "type": "lake",
            "location": "Chicago, USA",
            "lat": 43.0,
            "lon": -87.0,
            "area_km2": 58016,
            "contamination_level": "medium",
            "detected_contaminants": ["industrial_waste", "plastic", "agricultural_runoff"],
            "water_quality_index": 65
        },
        {
            "id": "usa_002",
            "name": "Mississippi River",
            "type": "river",
            "location": "Louisiana, USA",
            "lat": 29.9511,
            "lon": -90.0715,
            "length_km": 3734,
            "contamination_level": "high",
            "detected_contaminants": ["agricultural_runoff", "industrial_waste", "plastic", "chemicals"],
            "water_quality_index": 52
        },
        {
            "id": "usa_003",
            "name": "Chesapeake Bay",
            "type": "bay",
            "location": "Maryland, USA",
            "lat": 38.0,
            "lon": -76.5,
            "area_km2": 11601,
            "contamination_level": "high",
            "detected_contaminants": ["agricultural_runoff", "sewage", "plastic", "nutrients"],
            "water_quality_index": 48
        },
        {
            "id": "usa_004",
            "name": "Colorado River",
            "type": "river",
            "location": "Arizona, USA",
            "lat": 36.0,
            "lon": -112.0,
            "length_km": 2334,
            "contamination_level": "medium",
            "detected_contaminants": ["agricultural_runoff", "salts", "industrial_waste"],
            "water_quality_index": 58
        }
    ],
    
    "canada": [
        {
            "id": "can_001",
            "name": "Lake Ontario",
            "type": "lake",
            "location": "Toronto, Canada",
            "lat": 43.7,
            "lon": -77.9,
            "area_km2": 18960,
            "contamination_level": "low",
            "detected_contaminants": ["microplastics", "nutrients"],
            "water_quality_index": 72
        }
    ],
    
    # EUROPE
    "uk": [
        {
            "id": "uk_001",
            "name": "Thames River",
            "type": "river",
            "location": "London, UK",
            "lat": 51.5074,
            "lon": -0.1278,
            "length_km": 346,
            "contamination_level": "medium",
            "detected_contaminants": ["sewage", "plastic", "pharmaceutical_waste"],
            "water_quality_index": 62
        }
    ],
    
    "france": [
        {
            "id": "fr_001",
            "name": "Seine River",
            "type": "river",
            "location": "Paris, France",
            "lat": 48.8566,
            "lon": 2.3522,
            "length_km": 777,
            "contamination_level": "medium",
            "detected_contaminants": ["sewage", "plastic", "industrial_waste"],
            "water_quality_index": 58
        }
    ],
    
    "italy": [
        {
            "id": "it_001",
            "name": "Tiber River",
            "type": "river",
            "location": "Rome, Italy",
            "lat": 41.9028,
            "lon": 12.4964,
            "length_km": 406,
            "contamination_level": "medium",
            "detected_contaminants": ["sewage", "plastic", "nutrients"],
            "water_quality_index": 55
        }
    ],
    
    # ASIA
    "china": [
        {
            "id": "chn_001",
            "name": "Yangtze River",
            "type": "river",
            "location": "Shanghai, China",
            "lat": 31.2304,
            "lon": 121.4737,
            "length_km": 6300,
            "contamination_level": "high",
            "detected_contaminants": ["industrial_waste", "agricultural_runoff", "plastic", "heavy_metals"],
            "water_quality_index": 45
        },
        {
            "id": "chn_002",
            "name": "Yellow River",
            "type": "river",
            "location": "Shandong, China",
            "lat": 37.5,
            "lon": 119.0,
            "length_km": 5464,
            "contamination_level": "critical",
            "detected_contaminants": ["industrial_waste", "heavy_metals", "chemicals", "plastic"],
            "water_quality_index": 32
        }
    ],
    
    "japan": [
        {
            "id": "jpn_001",
            "name": "Tokyo Bay",
            "type": "bay",
            "location": "Tokyo, Japan",
            "lat": 35.6762,
            "lon": 139.6503,
            "area_km2": 922,
            "contamination_level": "medium",
            "detected_contaminants": ["industrial_waste", "plastic", "sewage"],
            "water_quality_index": 60
        }
    ],
    
    "thailand": [
        {
            "id": "tha_001",
            "name": "Chao Phraya River",
            "type": "river",
            "location": "Bangkok, Thailand",
            "lat": 13.7563,
            "lon": 100.5018,
            "length_km": 372,
            "contamination_level": "high",
            "detected_contaminants": ["sewage", "industrial_waste", "plastic", "organic_waste"],
            "water_quality_index": 42
        }
    ],
    
    # AFRICA
    "egypt": [
        {
            "id": "egy_001",
            "name": "Nile River",
            "type": "river",
            "location": "Cairo, Egypt",
            "lat": 30.0444,
            "lon": 31.2357,
            "length_km": 6650,
            "contamination_level": "high",
            "detected_contaminants": ["sewage", "agricultural_runoff", "industrial_waste", "plastic"],
            "water_quality_index": 48
        }
    ],
    
    "south_africa": [
        {
            "id": "za_001",
            "name": "Orange River",
            "type": "river",
            "location": "Cape Town, South Africa",
            "lat": -28.5,
            "lon": 16.5,
            "length_km": 2200,
            "contamination_level": "medium",
            "detected_contaminants": ["agricultural_runoff", "mining_waste", "plastic"],
            "water_quality_index": 56
        }
    ],
    
    # SOUTH AMERICA
    "brazil": [
        {
            "id": "bra_001",
            "name": "Amazon River",
            "type": "river",
            "location": "Manaus, Brazil",
            "lat": -3.1190,
            "lon": -60.0217,
            "length_km": 6400,
            "contamination_level": "low",
            "detected_contaminants": ["deforestation_runoff", "mercury", "plastic"],
            "water_quality_index": 68
        },
        {
            "id": "bra_002",
            "name": "Guanabara Bay",
            "type": "bay",
            "location": "Rio de Janeiro, Brazil",
            "lat": -22.9068,
            "lon": -43.1729,
            "area_km2": 412,
            "contamination_level": "critical",
            "detected_contaminants": ["sewage", "industrial_waste", "plastic", "oil"],
            "water_quality_index": 28
        }
    ],
    
    "argentina": [
        {
            "id": "arg_001",
            "name": "Riachuelo River",
            "type": "river",
            "location": "Buenos Aires, Argentina",
            "lat": -34.6037,
            "lon": -58.3816,
            "length_km": 64,
            "contamination_level": "critical",
            "detected_contaminants": ["industrial_waste", "heavy_metals", "sewage", "toxic_chemicals"],
            "water_quality_index": 22
        }
    ],
    
    # AUSTRALIA
    "australia": [
        {
            "id": "aus_001",
            "name": "Sydney Harbour",
            "type": "bay",
            "location": "Sydney, Australia",
            "lat": -33.8688,
            "lon": 151.2093,
            "area_km2": 55,
            "contamination_level": "low",
            "detected_contaminants": ["plastic", "sewage", "stormwater_runoff"],
            "water_quality_index": 70
        },
        {
            "id": "aus_002",
            "name": "Murray River",
            "type": "river",
            "location": "Victoria, Australia",
            "lat": -36.0,
            "lon": 144.0,
            "length_km": 2508,
            "contamination_level": "medium",
            "detected_contaminants": ["agricultural_runoff", "salts", "blue_green_algae"],
            "water_quality_index": 58
        }
    ],
    
    # MIDDLE EAST
    "uae": [
        {
            "id": "uae_001",
            "name": "Dubai Creek",
            "type": "creek",
            "location": "Dubai, UAE",
            "lat": 25.2769,
            "lon": 55.3340,
            "length_km": 14,
            "contamination_level": "medium",
            "detected_contaminants": ["sewage", "plastic", "oil"],
            "water_quality_index": 60
        }
    ],
    
    # SOUTHEAST ASIA
    "indonesia": [
        {
            "id": "idn_001",
            "name": "Citarum River",
            "type": "river",
            "location": "West Java, Indonesia",
            "lat": -6.9175,
            "lon": 107.6191,
            "length_km": 300,
            "contamination_level": "critical",
            "detected_contaminants": ["industrial_waste", "textile_dyes", "heavy_metals", "plastic", "sewage"],
            "water_quality_index": 18
        }
    ],
    
    "philippines": [
        {
            "id": "phl_001",
            "name": "Pasig River",
            "type": "river",
            "location": "Manila, Philippines",
            "lat": 14.5995,
            "lon": 120.9842,
            "length_km": 25,
            "contamination_level": "critical",
            "detected_contaminants": ["sewage", "industrial_waste", "plastic", "solid_waste"],
            "water_quality_index": 25
        }
    ]
}


@router.get("/location")
async def search_by_location(query: str):
    """
    Search for water bodies by location name
    
    Args:
        query: Location name (e.g., "Telangana", "Hyderabad")
    
    Returns:
        List of water bodies with contamination analysis
    """
    query_lower = query.lower().strip()
    
    # Search in location database
    results = []
    for location, water_sources in LOCATION_WATER_SOURCES.items():
        if query_lower in location or location in query_lower:
            results.extend(water_sources)
    
    # If no exact match, search in individual water source locations
    if not results:
        for location, water_sources in LOCATION_WATER_SOURCES.items():
            for source in water_sources:
                if query_lower in source["location"].lower() or query_lower in source["name"].lower():
                    if source not in results:
                        results.append(source)
    
    # Generate contamination summary
    total_sources = len(results)
    contamination_summary = {
        "critical": 0,
        "high": 0,
        "medium": 0,
        "low": 0
    }
    
    for source in results:
        contamination_summary[source["contamination_level"]] += 1
    
    # Categorize by type
    types_found = {}
    for source in results:
        water_type = source["type"]
        if water_type not in types_found:
            types_found[water_type] = 0
        types_found[water_type] += 1
    
    # Overall assessment
    avg_quality = sum(s["water_quality_index"] for s in results) / total_sources if total_sources > 0 else 0
    
    return {
        "search_query": query,
        "total_sources_found": total_sources,
        "types_found": types_found,
        "contamination_summary": contamination_summary,
        "overall_water_quality_index": round(avg_quality, 1),
        "water_sources": results,
        "recommendations": generate_recommendations(results, contamination_summary)
    }


@router.get("/location/{location_name}/details")
async def get_location_detailed_analysis(location_name: str):
    """
    Get detailed contamination analysis and solutions for a location
    
    Args:
        location_name: Name of the location
    
    Returns:
        Comprehensive analysis with solutions
    """
    location_lower = location_name.lower().strip()
    water_sources = LOCATION_WATER_SOURCES.get(location_lower, [])
    
    if not water_sources:
        # Try to find in nested locations
        for loc, sources in LOCATION_WATER_SOURCES.items():
            if location_lower in loc:
                water_sources = sources
                break
    
    # Detailed analysis
    total_sources = len(water_sources)
    
    # Contamination breakdown
    all_contaminants = {}
    for source in water_sources:
        for contaminant in source["detected_contaminants"]:
            if contaminant not in all_contaminants:
                all_contaminants[contaminant] = 0
            all_contaminants[contaminant] += 1
    
    # Priority sources needing immediate attention
    priority_sources = [s for s in water_sources if s["contamination_level"] in ["critical", "high"]]
    
    # Calculate total cleanup cost (INR)
    estimated_costs = {
        "river": 150000,  # ₹1.5L per km
        "lake": 500000,   # ₹5L per lake
        "reservoir": 1200000,  # ₹12L per reservoir
        "dam": 800000,    # ₹8L per dam
        "pond": 5800      # ₹5.8K per pond
    }
    
    total_cost = 0
    for source in priority_sources:
        base_cost = estimated_costs.get(source["type"], 100000)
        multiplier = 2 if source["contamination_level"] == "critical" else 1.5
        total_cost += base_cost * multiplier
    
    return {
        "location": location_name,
        "total_water_sources": total_sources,
        "water_sources": water_sources,
        "contamination_analysis": {
            "priority_sources": len(priority_sources),
            "common_contaminants": dict(sorted(all_contaminants.items(), key=lambda x: x[1], reverse=True)),
            "most_affected_type": max(
                {s["type"]: sum(1 for x in water_sources if x["type"] == s["type"]) for s in water_sources}.items(),
                key=lambda x: x[1]
            )[0] if water_sources else None
        },
        "immediate_actions_required": priority_sources,
        "estimated_cleanup_cost_inr": total_cost,
        "solutions": generate_detailed_solutions(water_sources, all_contaminants)
    }


def generate_recommendations(sources: List[dict], contamination_summary: dict) -> List[str]:
    """Generate recommendations based on contamination data"""
    recommendations = []
    
    if contamination_summary["critical"] > 0:
        recommendations.append(f"🚨 URGENT: {contamination_summary['critical']} water source(s) in CRITICAL condition - Immediate government intervention required")
    
    if contamination_summary["high"] > 0:
        recommendations.append(f"⚠️ {contamination_summary['high']} water source(s) with HIGH contamination - Start cleanup operations within 30 days")
    
    if contamination_summary["medium"] > 0:
        recommendations.append(f"⚡ {contamination_summary['medium']} water source(s) with MEDIUM contamination - Regular monitoring and preventive measures needed")
    
    # Specific contaminant recommendations
    all_contaminants = set()
    for source in sources:
        all_contaminants.update(source["detected_contaminants"])
    
    if "sewage" in all_contaminants:
        recommendations.append("🏭 Install sewage treatment plants and prevent untreated discharge")
    
    if "industrial_waste" in all_contaminants:
        recommendations.append("🏢 Enforce strict industrial waste management regulations")
    
    if "plastic" in all_contaminants:
        recommendations.append("♻️ Implement plastic ban and organize regular cleanup drives")
    
    if "heavy_metals" in all_contaminants:
        recommendations.append("⚗️ Set up water treatment facilities with heavy metal removal systems")
    
    if "agricultural_runoff" in all_contaminants:
        recommendations.append("🌾 Promote organic farming and create buffer zones around water bodies")
    
    return recommendations


def generate_detailed_solutions(sources: List[dict], contaminants: dict) -> dict:
    """Generate detailed solutions for the location"""
    
    solutions = {
        "immediate_actions": [],
        "short_term": [],
        "long_term": [],
        "prevention_measures": []
    }
    
    # Immediate actions based on severity
    critical_sources = [s for s in sources if s["contamination_level"] == "critical"]
    if critical_sources:
        for source in critical_sources:
            solutions["immediate_actions"].append({
                "source": source["name"],
                "action": "Emergency cleanup and water supply restriction",
                "timeline": "0-7 days",
                "cost_inr": 500000
            })
    
    # Short-term solutions (1-6 months)
    if "sewage" in contaminants:
        solutions["short_term"].append({
            "issue": "Sewage contamination",
            "solution": "Install temporary sewage treatment units and stop illegal discharge",
            "timeline": "1-3 months",
            "cost_inr": 2500000,
            "effectiveness": "85%"
        })
    
    if "plastic" in contaminants:
        solutions["short_term"].append({
            "issue": "Plastic pollution",
            "solution": "Deploy floating barriers and organize volunteer cleanup drives",
            "timeline": "2-4 months",
            "cost_inr": 180000,
            "effectiveness": "75%"
        })
    
    if "industrial_waste" in contaminants:
        solutions["short_term"].append({
            "issue": "Industrial pollution",
            "solution": "Enforce zero liquid discharge policy and install effluent treatment plants",
            "timeline": "3-6 months",
            "cost_inr": 5000000,
            "effectiveness": "90%"
        })
    
    # Long-term solutions (6+ months)
    solutions["long_term"].append({
        "project": "Comprehensive River Rejuvenation",
        "description": "Full-scale restoration with bioremediation and ecosystem revival",
        "timeline": "12-24 months",
        "cost_inr": 50000000,
        "benefits": ["Clean water supply", "Biodiversity restoration", "Tourism potential", "Flood control"]
    })
    
    solutions["long_term"].append({
        "project": "Smart Water Quality Monitoring",
        "description": "IoT sensors for real-time pollution tracking and alerts",
        "timeline": "6-12 months",
        "cost_inr": 8000000,
        "benefits": ["Early detection", "Data-driven decisions", "Public awareness", "Legal enforcement"]
    })
    
    # Prevention measures
    solutions["prevention_measures"] = [
        "Ban single-use plastics in 5km radius of water bodies",
        "Mandatory rainwater harvesting for all buildings",
        "Create 100m green buffer zones around all water bodies",
        "Weekly community monitoring and cleanup programs",
        "Strict penalties for illegal dumping (₹1L fine + jail)",
        "Public awareness campaigns in schools and colleges",
        "Promote eco-tourism to generate funds for maintenance",
        "Implement 'Adopt a Water Body' program for corporates"
    ]
    
    return solutions


@router.get("/all-water-sources")
async def get_all_water_sources(
    limit: Optional[int] = None,
    contamination_level: Optional[str] = None
):
    """
    Get all water sources from around the world
    
    Args:
        limit: Maximum number of results (optional)
        contamination_level: Filter by contamination level (critical/high/medium/low)
    
    Returns:
        All water sources globally
    """
    # Collect all water sources from all locations
    all_sources = []
    
    # Add comprehensive Indian water sources
    all_sources.extend(COMPREHENSIVE_INDIAN_SOURCES)
    
    # Add regional specific sources
    for location, sources in LOCATION_WATER_SOURCES.items():
        all_sources.extend(sources)
    
    # Filter by contamination level if specified
    if contamination_level:
        all_sources = [s for s in all_sources if s.get("contamination_level") == contamination_level]
    
    # Apply limit if specified
    if limit:
        all_sources = all_sources[:limit]
    
    return {
        "total": len(all_sources),
        "water_sources": all_sources,
        "timestamp": "2025-12-08T00:00:00Z"
    }
