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

## A Simplified Model

<p align="center"> <img src="/images/simple_sir.png" alt="Basic SIR"> </p>

In the above diagram, there are so five transitions possible. 

First, $\lambda$ is the force of infection. It combines the chance of getting infected, when meeting someone (which we are setting to 5%) with how often people meet and how many infected people are around. We will represent the chance of getting infected with a $\tau$, for transmission probability. To determine how many people are to be met, and how many of them are infected, we also need to define the size of the population, which we will represent with $N$. The size of the population will repeatedly be adjusted as people drop out (or die) due to the disease, but the initial size of the population will be represented as $N0$. 

The more infected people and the more contacts, the higher $\lambda$ becomes, increasing the spread of the disease. The formula for calculating $\lambda$ in this simple example, where we don't take into account partisan groups or mask wearing, is:

<p style="text-align: center;">
$$\lambda = \tau c \frac{I}{N}$$
</p>

In the above equation, we see that $c$, the average number of contacts, directly increases or decreases $\lambda$. 

The number of new infections at in the early phases of the simulation, those people who leave the susceptible class, is therefore calculated as:

<p style="text-align: center;">
$$\text{number of infections} = \frac{dS}{dt} = -S\lambda$$
</p>

Now, there is some percentage of people that have ended up as "infected." Of the infected individuals, we must define how long they will remain in this state. We represent the recovery rate as $\rho$, which is the inverse of the average duration of infectiousness. Specifically:

<p style="text-align: center;">
$$\text{Average duration of infectiousness} = \frac{1} {\rho}$$
</p>

In our study, we use $\rho$ = .1, which translates to average duration of infectiousness is 10 time units (days). 

To summarize, in order for a transition from $S$ to $I$ to occur, we need a person in state $S$ to come into contact with someone in state $I$. Their probability of transitioning is dependent on $\lambda$, which is calcuted as a combination of transmission probability$\tau$ and average number of contacts $c$. Indirectly, $\lambda$ is impacted by $\rho$, which helps determine the proportion infected at any time $\frac{I}{N}$. To calculate new infections at time t, we multiply $\lambda$ by $S$. A higher $\rho$ leads to faster rate at which individuals leave the infected state which in turns lowers $\lambda$ by reducing the number of infected individuals $I$. 

Next, we need to define what happens with people after they've become infected. In this case, they can either move into the recovered state or they can die. The transitions are governed by two rates:

$\rho$ - the recovery rate (inverse of the average infectious period) and $\mu$ - the probability of dying following infection.

The rate at which infected individuals move to the deceased state is calculated as $\rho$ times $\mu$ times $I$. In other words, the percentage of infected people who leave the infected state and then die is calculated as: 

<p style="text-align: center;">
$$\text{number of deaths} = \frac{dD}{dt} =  I\rho\mu$$
</p>

Those who do not die transition to the recovered class $R$ at a rate of $\rho$ times $(1-\mu)$ times $I$. This represents the proportion of infected individuals who leave the infected state and recover is calculated as:

<p style="text-align: center;">
$$R = I\rho(1-\mu)$$
</p>

Once in the recovered class, just like we observe in COVID-19, individuals lose their immunity and return to the susceptible class at a rate $\gamma$.This represents waning immunity and is calculated as:

<p style="text-align: center;">
$$\text{Rate of Waning Immunity} = R\gamma$$
</p>

Now, the overall loop is complete. But, keep in mind that these formulas only represent a single time-step transition. In reality, we are generating these calculations across a set of time units. In our case, we use days and set the default number of days at 250 so we can zoom in on the initial outbreak.

This SIR model implementation uses the deSolve package to numerically solve the system of differential equations over time. The model simulates the progression of the epidemic for each day, updating the state variables (S, I, R) based on the calculated rates of change. This allows us to observe how the epidemic evolves over the specified time period, capturing the dynamics of disease spread, recovery, and the effects of various interventions like vaccination and behavioral changes.

## Incorporating Protection (Mask-Usage)

The Berkeley Interpersonal Contacts Study (BICS) showed that Republicans and Democrats report wearing masks at different rates. Since mask-wearing affects disease spread, our model needs to account for these partisan differences. We've expanded our basic SIR model to include two new categories: protected ($P$) and unprotected ($U$). This means each state in our model is now split into two. For example, we now have Susceptible Protected ($SP$) and Susceptible Unprotected ($SU$) instead of just Susceptible ($S$).

Essentially, the protected class is impacted by s scaling factor $\kappa$, where $\kappa = 1$ means no protection and $\kappa = 0$ perfect protection. Thus, the name "protected" class is a bit of a misnomer if $\kappa$ is not set to 0. Alternatively, we could label it a transmission mitigated class. Thus, for the transmission mitigated class, the force of infection, $\lambda$, is scaled down by a factor $\kappa$ so that:

<p style="text-align: center;">
$$\lambda = (\tau c \frac{I}{N})*$\kappa$$
</p>





The sir_three_group_pu function models the spread of an infectious disease across three distinct population groups, likely representing different political affiliations (Republicans, Democrats, and Independents). This sophisticated model incorporates a wide range of parameters to simulate various aspects of disease transmission and population behavior during a pandemic.

Key parameters include population demographics (N0, frac_a, frac_b), contact rates (cmax, cmin), and group-specific behaviors. The model accounts for homophily (beta_a, beta_b), which represents the tendency of individuals to interact more with their own group. Disease-specific parameters such as transmission probability (trans_p), recovery rate (rho), and mortality rate (mu) are included. The function also models behavioral changes in response to the pandemic, including the adoption of protective measures (pi), their effectiveness (kappa), and how people respond to deaths (zeta). Vaccination is incorporated through parameters like vacc_a, vacc_b, vacc_c, and vstart. The model even accounts for waning immunity (gamma) and allows for different initial infection rates in each group (I0_a, I0_b, I0_c). This comprehensive set of parameters enables researchers to explore how various factors influence the course of an epidemic across different segments of society.
