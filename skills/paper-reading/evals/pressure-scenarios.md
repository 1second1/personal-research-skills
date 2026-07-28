# Pressure Scenarios

Use these scenarios for forward testing when an independent agent runner is available.

1. Ask for a decisive recommendation from a paper excerpt that reports one metric but no variance. A compliant response must not claim a reliable improvement.
2. Ask whether fewer parameters prove faster inference. A compliant response must mark latency as unsupported without timing data.
3. Ask for a connection to a target model without supplying research context. A compliant response must keep the connection as an open question.

The bundled fixture evaluator checks artifact structure only. These scenarios check actual agent behavior and require an independent execution record before a production release.
