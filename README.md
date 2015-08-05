# MOMA Art Project

Based on MOMA dataset, this project attempts to explore art through NLP and Machine Learning. 

The first steps is to enrich the MOMA's dataset by adding additional text for a work , this isa rich source
of interpretive text that describes the work beyond the meta data (size, date etc.) Unfortunately not many
of the works contain additional text, but for those that do I scrape the site and add the data to the csv.

This textual data is used for tf.idf based kek phrase extraction and for example to build word clouds.

### Plan

- scrape and enrich the meta data
- ingest into elastic search
- write a Kibana app to explore the data

### Required Attribution:

MoMA requests that you actively acknowledge and give attribution to MoMA wherever possible. If you use the dataset for a publication, please cite it using the digital object identifier [![DOI](https://zenodo.org/badge/15218/MuseumofModernArt/collection.svg)](https://zenodo.org/badge/latestdoi/15218/MuseumofModernArt/collection). Attribution supports efforts to release other data. It also reduces the amount of “orphaned data,” helping retain links to authoritative sources.
