---
title: 'Understanding the Three-Group SIR Used in Our Upcoming Paper'
date: 2024-12-20
permalink: /posts/2024/20/three-group-sir-partisan-groups/
tags:
  - Partisanship
  - Disease Transmission
  - Research
---

In our upcoming paper, "Measuring and Modeling the Impact of Partisan Differences in Health Behaviors on COVID-19 Dynamics," we use a three-group Susceptible-Infected-Recovered model to highlight the importance of incorporating partisan differences into models of disease transmission. In this blog post, I want to fully explain what is happening in the background for readers who may be interested in utlizing it themselves. For those users, we also built an R shiny app (soon to be published as well). The link to the shiny app will be: here.

There is a lot to unpack here, so let's start with the basic conceptualization of how the model will work. 
![Door Knocking](/images/simple_sir.png)

In the above diagram, there are so far three parameters that facilitate the transition between the three states. 

First, $\lambda$ is the force of infection. It combines the chance of getting infected when meeting someone (which we are setting to 5%) with how often people meet and how many infected people are around. The more infected people and the more contacts, the higher $\lambda$ becomes, increasing the spread of the disease. The formula for calculating $\lambda$ in this simple example, where we don't take into account partisan groups, is:

$
\lambda = \tau \sum_c_{1i} \left(\frac{IU_i}{N_i}
$


Second, there's $\mu_i$ - probability of dying following infection for group.

Lastly, there's $\gamma$ - rate of waning immunity.

Let's start with defining the function:

```{r}
sir_three_group_pu <- function(## parameters related to popn
                               N0 = 10000000, # population size
                               frac_a = 0.33, # fraction of population in group A
                               frac_b = 0.33, # fraction of population in group B
                               ## parameters related to contacts
                               cmax = NA, # initial/max average number of contacts per day (specify only if its the same for both groups, otherwise NA)
                               cmax_a = 8, cmax_b = 8, cmax_c=8, # initial/max average number of contacts per day by group 
                               cmin = NA, # min average contact
                               cmin_a = 3, cmin_b = 3, cmin_c=3,
                               beta_a=1, # homophily parameter for group a (beta_a = 1 means unbiased mixing; bigger values mean homophily) 
                               beta_b=1, # homophily parameter for group b (beta_b = 1 means unbiased mixing; bigger values mean homophily) 
                               #h_a=.5, # proportion of group A's total contact with members of their own group 
                               #h_b=.5, # proportion of group A's total contact with members of their own group 
                               ##
                               zeta = NA, # responsiveness of contact to deaths
                               zeta_a = 0.01, zeta_b = 0, zeta_c = 0.005,
                               trans_p = 0.05, # probability of transmission given contact (or susceptibility to infection given contact)
                               rho=1/10,# 1 / infectious period  or recovery rate
                               mu = NA,# probability of dying following infection
                               mu_a = 0.01, mu_b = 0.01, mu_c = .01, # can let it differ between groups to crudely account for difference in age composition between groups
                               kappa=0.9, # scaling factor for probability of transmission given contact resulting from protective behavior; kappa=1 means no protection, kappa = 0 means perfect protection
                               phi = NA, # waning of protective behavior
                               phi_a = 0, phi_b=0, phi_c=0,
                               I0_a=1, I0_b=1, I0_c=1, #intial infected in each group
                               time = 500, # time steps for simulation
                               pi = NA, # background rate of adopting protective behavior
                               pi_a = 0.05, pi_b = 0.05, pi_c = 0.05,
                               ell = 1, # time window for considering deaths that influence adoption of protective behavior
                               vacc = NA, # vaccination rate (goes from S to R)
                               # in Roubenoff et al. we assume about 2 million daily doses are distributed which is ~ 0.6 % of the population per day
                               vacc_a = 0.006, vacc_b = 0.006, vacc_c = 0.006,
                               vstart = 365, # start of vaccination
                               gamma = 1/182.5, # wanning immunity
                               
                               get_params=FALSE)
```

The sir_three_group_pu function models the spread of an infectious disease across three distinct population groups, likely representing different political affiliations (Republicans, Democrats, and Independents). This sophisticated model incorporates a wide range of parameters to simulate various aspects of disease transmission and population behavior during a pandemic.

Key parameters include population demographics (N0, frac_a, frac_b), contact rates (cmax, cmin), and group-specific behaviors. The model accounts for homophily (beta_a, beta_b), which represents the tendency of individuals to interact more with their own group. Disease-specific parameters such as transmission probability (trans_p), recovery rate (rho), and mortality rate (mu) are included. The function also models behavioral changes in response to the pandemic, including the adoption of protective measures (pi), their effectiveness (kappa), and how people respond to deaths (zeta). Vaccination is incorporated through parameters like vacc_a, vacc_b, vacc_c, and vstart. The model even accounts for waning immunity (gamma) and allows for different initial infection rates in each group (I0_a, I0_b, I0_c). This comprehensive set of parameters enables researchers to explore how various factors influence the course of an epidemic across different segments of society.
