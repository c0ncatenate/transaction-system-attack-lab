# Overview

The **Transaction System Attack Lab** is a deliberately vulnerable environment that models a
simplified multi-service transaction platform. The purpose of the lab is to explore how:

- design decisions,
- implementation mistakes, and
- logging/detection gaps

can combine into realistic **attack paths** across multiple services.

The lab is intentionally small and self-contained, so it can be:

- run locally for experimentation,
- used as a teaching aid for security engineering and penetration testing, and
- extended with additional scenarios over time.

The patterns in this lab are inspired by issues seen in modern transaction and financial-style
platforms, but the code and architecture are generic and not based on any specific real system.
