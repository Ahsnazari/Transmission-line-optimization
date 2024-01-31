import pypsa, numpy as np
import random
# marginal costs in EUR/MWh
marginal_costs = {"Wind": 0, "Hydro": 0, "Coal": 30, "Gas": 60, "Oil": 80, "Nuclear":10, "Solar": 0}

# power plant capacities (nominal powers in MW) in each country (not necessarily realistic)
power_plant_p_nom = {
    "Iran": {"Hydro": 12000, "Gas": 60000, "Nuclear": 1000},
    "Iraq": {
        "Oil": 5415, "Gas": 2181, "Hydro": 2518,
    },
    "Turkey": {
        "Hydro": 31500, "Gas": 25750, "Coal": 20000, "Solar": 8000, "Wind": 10590
    },
}




# country electrical loads in MW (not necessarily realistic)
loads = {"Iran": 70000, "Turkey": 45000, "Iraq": 27300}

# transmission capacities in MW (not necessarily realistic)

transmission = {
    "Iran": {"Turkey": 0, "Iraq": 0},
    "Turkey": {"Iraq": 18000},
}

network = pypsa.Network()

countries = ["Iran", "Turkey","Iraq"]

for country in countries:
    network.add("Bus", country)

    for tech in power_plant_p_nom[country]:
        network.add(
            "Generator",
            "{} {}".format(country, tech),
            bus=country,
            p_nom=power_plant_p_nom[country][tech],
            marginal_cost=marginal_costs[tech],
        )

    network.add("Load", "{} load".format(country), bus=country, p_set=loads[country])

    # add transmission as controllable Link
    if country not in transmission:
        continue

    for other_country in countries:
        if other_country not in transmission[country]:
            continue

        # NB: Link is by default unidirectional, so have to set p_min_pypu = -1
        # to allow bidirectional (i.e. also negative) flow
        network.add(
            "Link",
            "{} - {} link".format(country, other_country),
            bus0=country,
            bus1=other_country,
            p_nom=transmission[country][other_country],
            p_min_pu=-1,
        )


network.optimize(solver_name = 'glpk')
print(f'cacities are as followed:',transmission['Iran'])
print(network.buses_t.marginal_price)
print(network.generators_t.p)
