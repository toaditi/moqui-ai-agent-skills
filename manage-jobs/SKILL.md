---
name: manage-jobs
description: Define and manage background and scheduled tasks in Moqui using ServiceJob.
---

# Skill: manage-jobs

## Goal
Efficiently schedule and manage background tasks in Moqui using the `ServiceJob` framework, ensuring reliable execution of periodic or deferred business processes.

## Triggers
**ALWAYS** read this skill when:
- Creating a new scheduled task (e.g., nightly sync, hourly cleanup).
- Configuring `moqui.service.job.ServiceJob` records in XML data files.
- Managing background job execution parameters and cron expressions.

## Use when
- Running periodic reports or data exports.
- Coordinating high-volume data synchronization with external systems.
- Deferring heavy processing away from UI requests.

## Don't use when
- The logic needs to be immediate and synchronous (use a standard service call).
- The action is a simple event response (use `manage-eca`).

## Inputs
- Service to be run as a job.
- Schedule frequency (cron expression or interval).
- Job parameters (in-map).

## Outputs
- `<moqui.service.job.ServiceJob>` records in XML data files (usually `data/*.xml`).

## Rules & Guardrails
1. **Job Definition**: Jobs are defined as data records (Entity: `moqui.service.job.ServiceJob`).
    - Required fields: `jobName`, `serviceName`.
2. **Job Parameters**: 
    - Use `<moqui.service.job.ServiceJobParameter>` child elements to define default values for the job's service.
    - Use parameters to store persistent state, such as `lastRunTime`, which the service can update at the end of its run.
3. **Scheduling**:
    - `cronExpression`: Standard cron format (e.g., `0 0 2 * * ?` for 2 AM daily).
    - `repeatCount`: Use `-1` for infinite repetition.
    - `repeatInterval`: Interval in milliseconds if cron is not used.
4. **Execution**:
    - Use `ec.service.job(jobName).run()` to trigger a defined job immediately.
    - Or use `ec.service.sync().name(serviceName).async().call()` for one-off background execution without a formal `ServiceJob` record.
5. **Monitoring**: Check `moqui.service.job.ServiceJobRun` for execution history and logs.

## Failure handling
- **State Management**: If a job fails, the `lastRunTime` parameter might not be updated. Ensure your service handles partial runs or can re-run from the last successful point.
- **Overlapping RUNS**: By default, Moqui ensures only one instance of a specific `ServiceJob` runs at a time.

## Minimal example
**Requirement**: Define a job with a persistent `lastRunTime` parameter.

**Good Output (XML Data File)**:
```xml
<entity-facade-xml>
    <moqui.service.job.ServiceJob jobName="FetchNewOrders" 
                                 serviceName="co.hotwax.oms.integration.OrderServices.fetch#NewOrders"
                                 cronExpression="0 0/15 * * * ?" 
                                 paused="N">
        <moqui.service.job.ServiceJobParameter parameterName="lastRunTime" parameterValue="2024-01-01 00:00:00.000"/>
    </moqui.service.job.ServiceJob>
</entity-facade-xml>
```
**In Groovy Service Logic**:
```groovy
// At the end of the service, update the job parameter
ec.service.sync().name("update#moqui.service.job.ServiceJobParameter")
    .inMap([jobName: jobName, parameterName: "lastRunTime", parameterValue: ec.user.nowTimestamp.toString()])
    .call()
```
