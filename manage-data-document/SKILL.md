---
name: manage-data-document
description: Define Moqui Data Documents for search indexing (ElasticSearch/Solr) and flattened data export.
---

# Skill: manage-data-document

## Goal
Define hierarchical but flattened data structures (Data Documents) in Moqui to simplify indexing for search engines and cross-system data synchronization.

## Triggers
**ALWAYS** read this skill when:
- Creating or modifying search index definitions (e.g., for ElasticSearch).
- Configuring a `DataFeed` that requires a specific data structure.
- You need a flattened Map representation of a complex entity graph.

## Use when
- Defining the fields to be indexed for a "Product" or "Order" search.
- Setting up a background data feed to an external system.
- Using `ec.entity.getDataDocuments()` to retrieve structured data.

## Don't use when
- Performing standard database joins for UI display (use `manage-entities` for static view-entities).
- Defining basic entity models.

## Inputs
- Primary entity name.
- Related entities and specific field paths.
- Index name and document name.

## Outputs
- `moqui.entity.document.DataDocument` and `moqui.entity.document.DataDocumentField` records (usually in an XML data file).

## Rules & Guardrails
1. **Primary Entity**: Every Data Document MUST have a `primaryEntityName`.
2. **Field Paths**: Use colon-separated relationship aliases to reach deep fields (e.g., `featureAppls:productFeatureId` or `items:description`).
3. **Field Aliasing**: Use `fieldNameAlias` to give descriptive names to fields, especially when multiple related entities have fields with the same name (e.g., `thruDate`).
4. **Sequencing**: Maintain `fieldSeqId` for consistent mapping and debugging.
5. **Index Association**: Use `indexName` to group documents intended for the same search index.
6. **Filtering**: Use `moqui.entity.document.DataDocumentCondition` records to restrict which primary entity records are included in the document (e.g., only include records where `statusId` is not `DELETED`).

## Failure handling
- **Missing Relationships**: If a field path is invalid, verify that the relationship `short-alias` is correctly defined in the entity XML.
- **Data Load Priority**: Ensure Data Documents are loaded as `seed` or `seed-initial` data to be available for background feeds.

## Minimal example
**Requirement**: Create a Data Document for 'Product' with its categories.

**Bad Output**:
```xml
<!-- Missing fieldPath detail and alias -->
<dataDocuments dataDocumentId="ProdDoc" primaryEntityName="Product">
    <fields fieldSeqId="01" fieldPath="productId"/>
    <fields fieldSeqId="02" fieldPath="productCategory"/>
</dataDocuments>
```

**Good Output**:
```xml
<dataDocuments dataDocumentId="ProductDoc" indexName="inventory" documentName="Product" primaryEntityName="mantle.product.Product">
    <fields fieldSeqId="01" fieldPath="productId"/>
    <fields fieldSeqId="02" fieldPath="productName"/>
    <!-- Use relationship alias 'categories' to reach categoryId -->
    <fields fieldSeqId="10" fieldPath="categories:productCategoryId" fieldNameAlias="categoryIds"/>
    <fields fieldSeqId="11" fieldPath="categories:thruDate" fieldNameAlias="categoryThruDate"/>
</dataDocuments>
```
