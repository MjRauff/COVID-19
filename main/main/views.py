from django.views import generic
from bs4 import BeautifulSoup
import requests
from bs4 import BeautifulSoup
class IndexView(generic.TemplateView):
    template_name = "index.html"

    def corona_time(self):
        source = requests.get("https://www.worldometers.info/coronavirus/").text
        soup = BeautifulSoup(source, "lxml")
        html_text = soup.find("tbody")
        stats = []
        check_dict = {" S. Korea ":"South Korea",
                      " USA ":"United States",
                      " UK ":"United Kingdom",
                      " UAE ":"United Arab Emirates",
                     }
        for x in html_text.find_all("tr"):
            w = x.find_all("td")
            country = w[0].text
            number = w[1].text
            new_cases = w[2].text
            total_deaths = w[3].text
            new_deaths = w[4].text
            total_recovered = w[5].text
            active_cases = w[6].text
            serious_critical = w[7].text
            cases_m1_pre = w[8].text
            if cases_m1_pre == "":
                cases_m1_pre = 0
            cases_m1 = float(cases_m1_pre)
            number_1 = number.replace(",","")
            if country in check_dict:
                stats.append((check_dict[country], number_1, new_cases, total_deaths, new_deaths, total_recovered, active_cases, serious_critical, cases_m1))
            else:
                stats.append((country, number_1, new_cases, total_deaths, new_deaths, total_recovered, active_cases, serious_critical, cases_m1))
        return stats


    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            stats = self.corona_time()
            context["stats"] = stats[:]
            context["stats2"] = stats[:10]
            return context

class TestView(generic.TemplateView):
    template_name = "test.html"
