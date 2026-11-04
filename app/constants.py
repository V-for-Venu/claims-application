from api.tag import Tag

expiry_in_seconds = 1800

fastClaims_description = "Application to Process the Claims with Provider Interface."
tags_metadata = [
    {
        "name": Tag.PROVIDERS.value,
        "description": "Operations related to Providers Including Login, Authentication & Authorization, Claim Creation.",
    },
    {
        "name": Tag.CLAIMS.value,
        "description": "Operations related to Claims Including Add, Read, Update and Delete Claims.",
    },
]
