import requests
import asyncio
import httpx

TOTAL_SUPPLY = 1_000_000_000
KAITO_ALLOCATION = 0.0035*TOTAL_SUPPLY
GALXE_ALLOCTION = 0.035*TOTAL_SUPPLY
SHARES = {
    "7d": 0.12 * KAITO_ALLOCATION,
    "30d": 0.16 * KAITO_ALLOCATION,
    "90d": 0.22 * KAITO_ALLOCATION,
    "180d": 0.24 * KAITO_ALLOCATION,
    "365d": 0.26 * KAITO_ALLOCATION
}

ROLE={
    'shihan':2,
    'senshi':1.75,
    'shugo':1.5,
    'deshi':1.25,
    'none':1
}


######### GALXE & DISCORD PART ##########


Total_loyalty_points=1113948000 #Updates Regularly

def get_loyalty_points(address, space_id=58934, season_id=None):
    if len(address)!=42:
        return None
    GALXE_URL = "https://graphigo.prd.galaxy.eco/query"
    HEADERS = {
        "Content-Type": "application/json",
        "Origin": "https://galxe.com",
        "Referer": "https://galxe.com/",
        "User-Agent": "Mozilla/5.0"
    }
    variables = {
        "id": space_id,
        "address": f"EVM:{address}"
    }
    if season_id is not None:
        variables["seasonId"] = season_id

    query = """
    query SpaceLoyaltyPoints($id: Int, $address: String!, $seasonId: Int) {
      space(id: $id) {
        id
        addressLoyaltyPoints(address: $address, sprintId: $seasonId) {
          id
          points
          rank
          __typename
        }
        __typename
      }
    }
    """

    payload = {
        "operationName": "SpaceLoyaltyPoints",
        "variables": variables,
        "query": query
    }

    response = requests.post(GALXE_URL, json=payload, headers=HEADERS)
    response.raise_for_status()
    result = response.json()
    if 'errors' in result:
        return None
    
    loyalty_points = result['data']['space']['addressLoyaltyPoints']['points']
    return loyalty_points

def get_address_allocation(address,role):
    loyalty_points = get_loyalty_points(address)
    if loyalty_points==None:
        return 'Allocation Not Found'
    address_allocation= ((loyalty_points*ROLE[role])/Total_loyalty_points)*GALXE_ALLOCTION
    return address_allocation


########### KAITO PART ############

async def fetch_data(client, window):
    url = "https://kaito.irys.xyz/api/community-mindshare"
    params = {"window": window}
    response = await client.get(url, params=params)
    response.raise_for_status()
    return window, response.json()

def calculate_allocations(username, data, window):
    share_amount = SHARES[window]
    allocation = 0
    yappers = data.get("community_mindshare", {}).get("top_1000_yappers", [])
    for user in yappers:
        if username.lower() == user.get("username").lower():
            mindshare = user.get("mindshare", 0)
            allocation = mindshare * share_amount
            break
    return allocation

async def get_kaito_allocation(username):
    timeframes = ["7d", "30d", "90d", "180d", "365d"]
    async with httpx.AsyncClient() as client:
        tasks = [fetch_data(client, tf) for tf in timeframes]
        responses = await asyncio.gather(*tasks)

    all_allocations = []
    for window, data in responses:
        alloc = calculate_allocations(username, data, window)
        all_allocations.append(alloc)
    
    return sum(all_allocations)

