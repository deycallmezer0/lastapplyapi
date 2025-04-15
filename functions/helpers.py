import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel


class Job(BaseModel):
    title: str
    company: str
    pay: str
    location: str
    requirements: str


async def extract_job_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    job_info = {}

    job_info["title"] = (
        soup.find(class_="sub-nav-cta__header").text.strip()
        if soup.find(class_="sub-nav-cta__header")
        else "N/A"
    )
    job_info["company"] = (
        soup.find(class_="sub-nav-cta__optional-url").text.strip()
        if soup.find(class_="sub-nav-cta__optional-url")
        else "N/A"
    )
    job_info["pay"] = (
        soup.find(class_="").text.strip() if soup.find(class_="") else "N/A"
    )
    job_info["location"] = (
        soup.find("span", class_="sub-nav-cta__meta-text").text.strip()
        if soup.find("span", class_="sub-nav-cta__meta-text")
        else "N/A"
    )

    requirements_elements = soup.find_all(
        class_="show-more-less-html__markup show-more-less-html__markup--clamp-after-5 relative overflow-hidden"
    )
    job_info["requirements"] = (
        " ".join([req.text.strip() for req in requirements_elements])
        if requirements_elements
        else "N/A"
    )

    return job_info


result = extract_job_info("https://www.linkedin.com/jobs/view/4199739366")

print(result)
