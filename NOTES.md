| Group            | RPS | Avg Response Time | Sentry          | New Relic       | Notes                                                                         |
| ---------------- | --- | ----------------- | --------------- | --------------- | ----------------------------------------------------------------------------- |
| health           | 79  | 21s/82s           | 9.6ms/14.7ms    | 601.5ms/721.9ms |                                                                               |
| consultation     | 2.9 | 58s/60s           | 397.9ms/598.5ms | 393ms/606ms     | Response time  rises constantly until the server crashers at about 1350 users |
| users            | 21  | 51s/58s           | 67ms/104ms      | 76ms/99ms       |                                                                               |
| patients         | 1.3 | 60s               | 707ms/935ms     | 700ms/2259ms    | crashes at 1600 users                                                         |
| facility         | 8.6 | 60s               | 102ms/141ms     | 108ms/145ms     | crashes when response times hit 60s                                           |
| daily_round      | 4.4 | 60s               | 145ms/202ms     | 150ms/227ms     | craashes at 1900 users                                                        |
| daily_round_post | 2.1 |                   |                 |                 |                                                                               |