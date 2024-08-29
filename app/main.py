import asyncio
from typing import Annotated, Union

import requests
from fastapi import FastAPI, status, Header, Response
from fastapi.middleware.cors import CORSMiddleware

from .schemas import Profile
from .prompts import rewrite_experience, write_responsibilities_for_experience


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    # allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)

URL = "https://quick-apply-b4e936c5c50c.herokuapp.com/api/v1/users/verifications"


@app.post("/build/", status_code=status.HTTP_201_CREATED)
async def build(profile: Profile, authorization: Annotated[Union[str, None], Header(name="Authorization")],
                response: Response):
    verification_response = requests.get(url=URL, headers={"Authorization": authorization})
    if verification_response.text == "OK":
        tasks = []
        for experience in profile.profile_experiences:
            if experience.experience_responsibilities is None:
                tasks.append(
                    write_responsibilities_for_experience(job_position=experience.position)
                )
            else:
                tasks.append(
                    rewrite_experience(
                        responsibilities=experience.experience_responsibilities, job_position=experience.position
                    )
                )

        rewritten_experiences = await asyncio.gather(*tasks)
        for experience, rewritten_experience in zip(profile.profile_experiences, rewritten_experiences):
            experience.experience_responsibilities = rewritten_experience.responsibilities

        return {"data": profile, "status": status.HTTP_201_CREATED}
    response.status_code = status.HTTP_401_UNAUTHORIZED
    return {"data": "Error", "status": status.HTTP_401_UNAUTHORIZED, "message": "Not Authorized"}



