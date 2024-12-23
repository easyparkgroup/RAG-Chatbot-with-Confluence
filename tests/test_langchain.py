from src.create_confluence_embeddings import create_embeddings_from_space_content

interesting_global_spaces = [
    "AAT",  # Android chapter
    "ACQ",  # Drivers Acquisition Team
    "ACT",  # Drivers Account Team
    "AE",  # Analytics Engineering
    "APT",  # Drivers Pay Team
    "APT1",  # Agile Project Team
    "AT",  # Architecture Team
    "B2B",  # B2B
    "B2BCore",  # B2B Core
    "B2BSRC",  # B2B Sales Service Request Center
    "B2CWEB",  # Driver's Web Parking
    "BA",  # B2B Acquisition
    "BAT",  # Business Analytics
    "BEC",  # BE Chapter
    "BOT",  # BraV Online Tutorials
    "BRAV",  # BraV
    "CCIS",  # Customer Care
    "CE",  # Corporation's Experience
    "COM",  # Communications
    "CR",  # Operator Finance
    "CRM",  # CRM & Leads
    "CVT2",  # Drivers Automotive Team
    "CW",  # Web Team
    "Comms",  # Comms
    "DACT",  # Drivers AI Chatbot Team
    "DAP",  # Data & Analytics Product Area
    "DAT",  # Driver's AppBFF Team
    "DCT",  # Drivers Charging Team
    "DEVXP",  # Developers Experience
    "DI",  # Analytics
    "DIS",  # Distribution
    "DISC",  # Drivers Discovery Team
    "DOT",  # Drivers Off-Street Team
    "DP",  # Data Platform
    "DPAT",  # Drivers Parking Team
    "DPT",  # Drivers Platform team
    "DQ",  # Data Quality
    "DS",  # Design System
    "DSCI",  # Data Science
    "EAT",  # Enterprise Agile Transformation
    "EMA",  # EMA | EPIC Modularization Agents
    "EP",  # The Curb
    "EPA",  # Drivers Experience
    "EPIC",  # Epic platform
    "EPM",  # External Product Migration
    "EPM2",  # External Product Migration 2
    "ERPTP",  # ERP Transformation Program
    "ET",  # Driver’s EV Charging Team (Back-end)
    "ETPM",  # Engineering Team Performance Management
    "ETPM1",  # Engineering Team Performance Management
    "FET",  # Financial Engineering Team
    "FIN",  # Finance
    "GATE",  # Gated parking services
    "GP",  # TOP GUN Global Platform
    "GPMO",  # Global PMO
    "GRID",  # GRID
    "IAM",  # IAM
    "IAT",  # iOS chapter
    "IDP",  # Internal Developer Platform
    "INFOSEC",  # Information Security, Risk and Compliance
    "IQ",  # InfoSec Queue
    "IT",  # Internal IT
    "ITSM",  # IT Support by Internal IT
    "Insights",  # Insights
    "KM",  # Kafka Migration
    "MARK",  # Global Marketing
    "MIG",  # Migration
    "OC",  # Order Core
    "OPS",  # OPS
    "PA",  # Product Analytics
    "PAYN",  # Drivers PayNow team
    "PAYNA",  # Payments North America
    "PC",  # People & Culture
    "PCT",  # ParkingCore Team
    "PDBRD",  # Parking Dashboard
    "PE",  # Parking Excellence
    "PERM",  # Permits project
    "PET",  # Platform Engineering
    "PKM",  # Parkimeter
    "PMO",  # Global PMO Projects
    "POPS",  # Parking Operator Support
    "PPACK",  # Product Packages
    "PRCT",  # Procurement
    "PRO",  # Productivity
    "PROC",  # Procurement
    "PRODSUP",  # Product Support
    "PayLater",  # PayLater
    "RBAC",  # Role-based access control
    "RES",  # Reservations
    "RND",  # Product & Technology
    "RT",  # RevOps Team
    "SBT",  # Shared Backend Team
    "SD",  # Insights Berlin - data acquisitions
    "SEC",  # Platform Security
    "SET",  # Service Enablement Team
    "SGT",  # Service Governance Team
    "SOM",  # Service Operations
    "Strategy",  # Strategy
    "T1",  # Epic Modularization Task force
    "T2TLL",  # PayCore
    "T3",  # T3
    "T4",  # T4
    "T5",  # Hubs
    "TGSP",  # TOP GUN Smart Proxy
    "TL",  # Legal
    "TM",  # Tariff Team
    "TNT",  # Transformation and Transition
    "TOLL",  # B2B Partnerships Team
    "USDPI",  # US Data Platform & Insights
    "UX",  # Product Design
    "WS",  # Web Self-Service
]

interesting_subset = [
    "DEVXP",  # Developers Experience
    "EP",  # The Curb
    "EPA",  # Drivers Experience
    "EPIC",  # Epic platform
    "ERPTP",  # ERP Transformation Program
    "PC",  # People & Culture
    "PE",  # Parking Excellence
    "PET",  # Platform Engineering
    "POPS",  # Parking Operator Support
    "PPACK",  # Product Packages
    "PRO",  # Productivity
    "RND",  # Product & Technology
    "~215070400",  # Frank's personal space
]

test_questions = [
    "what is 'Epic'?",
    "who is the CTO of EasyPark?",
    "where can I learn more about the cluster model?",
    "what is EasyPark's strategy for 2025?" "is there a nice Pizza place near the Basingstoke office?",
    "what is the ERP system and how do I get access to it?",
    "how do I do expense reports?",
    "how do I get access to Snowflake?",
    "what teams are there in P&T?",
    "what's the address to the Atlanta office and how do I get in there?",
    "how can I do canary deploys for my service?",
]


def test_create_embeddings_from_space_content():
    print()
    create_embeddings_from_space_content("RND")
