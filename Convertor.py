from bs4 import BeautifulSoup
import requests
import csv

def convert(group, fileName):
    companies = []
    URLs = []
    baseURL = "https://techdayhq.com/community/startups/"
    descriptions = []
    socialLinks = []

    heading = group.find("div", class_="section-heading")
    for child in heading.find_all("div"):
        child.decompose()
    heading = heading.text

    for company in group.findAll("div", class_="company"):
        companyName = company.find("div", class_="name").text.strip('\n')
        companies.append(companyName)
        href = company.find('a', href=True)
        if "company" not in href['href']:
            url = href['href'].replace("/companies/", "")

        visitURL = baseURL + url
        URLs.append(visitURL)
        description = ""
        try:
            rec = requests.get(visitURL)
            soupCompany = BeautifulSoup(rec.content, "html.parser")
            paragraphs = soupCompany.find("div", class_="description")
            for p in paragraphs.findAll("p"):
                description += p.text + "\n"
            links = soupCompany.find("div", class_="social-icons")
            socials = ""
            for a in links.find_all('a', href=True):
                socials += a['href'] + "\n"


        except:
            description = "ERROR"
            socials = "ERROR"
        descriptions.append(description)
        socialLinks.append(socials)
    fileName += '.csv'
    with open(fileName , 'w') as csvfile:
        filewriter = csv.writer(csvfile)
        csvfile.write(heading + '\n')
        filewriter.writerow(companies)
        filewriter.writerow(URLs)
        filewriter.writerow(descriptions)
        filewriter.writerow(socialLinks)

    return


r = requests.get("https://techdayhq.com/new-york/participants")
soup = BeautifulSoup(r.content, "html.parser")

allCompanies = soup.find("div", class_="companies")
file = 'file'
for companiesGroup in allCompanies.findAll("div", class_="section"):
    convert(companiesGroup, file)
    file += 'e'