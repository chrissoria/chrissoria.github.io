---
title: "Understanding the Three-Group SIR Used in Our Upcoming Paper"
date: "2024-12-20"
permalink: "/posts/2024/20/three-group-sir-partisan-groups/"
tags:
- Partisanship
- Disease Transmission
- Research
---

In our upcoming paper, "Measuring and Modeling the Impact of Partisan Differences in Health Behaviors on COVID-19 Dynamics," we use a three-group Susceptible-Infected-Recovered model to highlight the importance of incorporating partisan differences into models of disease transmission. In this blog post, I want to fully explain what is happening in the background for readers who may be interested in utlizing it themselves. For those users, we also built an R shiny app (soon to be published as well). The link to the shiny app will be: here.

There is a lot to unpack here, so let's start with the basic conceptualization of how the model. 

<p align="center"> <img src="/images/simple_sir.png" alt="Basic SIR"> </p>

In the above diagram, there are so far three parameters that facilitate the transition between the three states. 

First, $\lambda$ is the force of infection. It combines the chance of getting infected, when meeting someone (which we are setting to 5%) with how often people meet and how many infected people are around. We will represent the chance of getting infected with a $\tau$, for transmission probability. To determine how many people are to be met, and how many of them are infected, we also need to define the size of the population, which we will represent with $N$. The size of the population will repeatedly be adjusted as people drop out (or die) due to the disease, but the initial size of the population will be represented as $N0$. 

The more infected people and the more contacts, the higher $\lambda$ becomes, increasing the spread of the disease. The formula for calculating $\lambda$ in this simple example, where we don't take into account partisan groups or mask wearing, is:

<p style="text-align: center;">
$$\lambda = \tau c \frac{I}{N}$$
</p>

In the above equation, we see that $c$, the average number of contacts, directly increases or decreases $\lambda$.

Now, there is some percentage of people that have ended up as "infected." Of the infected individuals, we must define how long they will remain in this state. We represent the recovery rate as $\rho$, which is the inverse of the average duration of infectiousness. Specifically:

<p style="text-align: center;">
$$\text{Average duration of infectiousness} = \frac{1} {\rho}$$
</p>

In our study, we use $\rho$ = .1, which translates to average duration of infectiousness is 10 time units (days). 

To summarize, in order for a transition from $S$ to $I$ to occur, we need a person in state $S$ to come into contact with someone in state $I$. Their probability of transitioning is dependent on $\lambda$, which is calcuted as a combination of transmission probability$\tau$ and average number of contacts $c$. Indirectly, $\lambda$ is impacted by $\rho$, which helps determine the proportion infected at any time $\frac{I}{N}$. To calculate new infections at time t, we multiply $\lambda$ by $S$. A higher $\rho$ leads to faster recovery which in turns lowers $\lambda$ by reducing the number of infected individuals. 

Next, we need to define what happens with people after they've become infected. In this case, they can either move into the recovered state or they can die. The transitions are governed by two rates:

$\rho$ - the recovery rate (inverse of the average infectious period)
$\mu$ - the probability of dying following infection

The rate at which infected individuals move to the deceased state is calculated as $\rho \mu I$. Those who do not die transition to the recovered class $R$ at a rate of $\rho(1-\mu)I$. Once in the recovered class, individuals may lose their immunity and return to the susceptible class at a rate $\gamma$, which represents waning immunity.











The sir_three_group_pu function models the spread of an infectious disease across three distinct population groups, likely representing different political affiliations (Republicans, Democrats, and Independents). This sophisticated model incorporates a wide range of parameters to simulate various aspects of disease transmission and population behavior during a pandemic.

Key parameters include population demographics (N0, frac_a, frac_b), contact rates (cmax, cmin), and group-specific behaviors. The model accounts for homophily (beta_a, beta_b), which represents the tendency of individuals to interact more with their own group. Disease-specific parameters such as transmission probability (trans_p), recovery rate (rho), and mortality rate (mu) are included. The function also models behavioral changes in response to the pandemic, including the adoption of protective measures (pi), their effectiveness (kappa), and how people respond to deaths (zeta). Vaccination is incorporated through parameters like vacc_a, vacc_b, vacc_c, and vstart. The model even accounts for waning immunity (gamma) and allows for different initial infection rates in each group (I0_a, I0_b, I0_c). This comprehensive set of parameters enables researchers to explore how various factors influence the course of an epidemic across different segments of society.
