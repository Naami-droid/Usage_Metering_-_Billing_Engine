

def simulate_token_count(text:str)->int:
    token_list=text.split(" ")
    return len(token_list)


def create_idempotency_key(request_id:str, usage_type:str)->str:
    return f"{request_id}_{usage_type}"