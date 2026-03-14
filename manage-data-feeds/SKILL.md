---
name: manage-data-feeds
description: Manage Moqui Data Feeds to orchestrate document synchronization to external services, queues, or search indexes.
---

# Skill: manage-data-feeds

## Goal
Orchestrate the real-time or periodic delivery of flattened Data Documents to external systems (Search Engines, REST APIs, Message Queues).

## Triggers
**ALWAYS** read this skill when:
- Configuring real-time data push to a search engine (Solr/ElasticSearch).
- Setting up a data synchronization bridge between Moqui and an external system.
- Defining `DataFeed` or `DataFeedDocument` records.

## Use when
- Triggering an external API call whenever an entity in a `DataDocument` changes.
- Pushing updates to a search index.
- Implementing a custom "receiver" service for processed data documents.

## Don't use when
- Simply querying data within Moqui (use `manage-entities` or `manage-view-entities`).
- Handling basic entity CRUD operations.

## Inputs
- `dataDocumentId`(s) to be fed.
- Receiver service name (`feedReceiveServiceName`).
- Feed type (Push vs. Poll).

## Outputs
- `moqui.entity.feed.DataFeed` and `moqui.entity.feed.DataFeedDocument` records (XML data).

## Rules & Guardrails
1. **Feed Type**:
   - Use `DTFDTP_RT_PUSH` for real-time updates (triggered immediately on transaction commit).
   - Use `DTFDTP_POLL` for scheduled or manual batch processing.
2. **Receiver Service**: The `feedReceiveServiceName` MUST accept a parameter named `document` (Map) or `documentList` (List of Maps).
3. **Selective Feeding**: Ensure the `DataDocument` associated with the feed only contains the fields necessary for the consumer to avoid overhead.
4. **Error Handling**: Monitor Moqui logs for failures in `feedReceiveServiceName`. Real-time feeds run after the main transaction; handle exceptions gracefully in the receiver to prevent log bloat.
5. **Delete Handling**: ALWAYS provide a `feedDeleteServiceName` if the consumer system needs to remove data when the primary entity is deleted.

## Failure handling
- **Feed Lag**: If high-volume updates cause performance issues, consider switching from real-time push to polling or using a message queue in the receiver service.

## Minimal example
**Requirement**: Push 'Product' updates to a Solr index in real-time.

**Bad Output**:
```xml
<!-- Missing feed type and delete service -->
<moqui.entity.feed.DataFeed dataFeedId="ProdFeed" feedReceiveServiceName="index#Solr">
    <documents dataDocumentId="ProductDoc"/>
</moqui.entity.feed.DataFeed>
```

**Good Output**:
```xml
<!-- Proper real-time push configuration -->
<moqui.entity.feed.DataFeed dataFeedId="ProductSolrFeed" 
        dataFeedTypeEnumId="DTFDTP_RT_PUSH"
        feedName="Product Solr Push Feed" 
        feedReceiveServiceName="co.hotwax.oms.search.SearchServices.index#ProductSolr"
        feedDeleteServiceName="org.moqui.search.SearchServices.delete#DataDocument">
    <documents dataDocumentId="ProductDoc"/>
</moqui.entity.feed.DataFeed>
```
