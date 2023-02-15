## Rendered.ai's SDK: anatools

`anatools` is an SDK for connecting to the Rendered.ai Platform.
With `anatools` you can generate and access synthetic datasets, and much more!

```python
>>> import anatools
>>> ana = anatools.client()
'Enter your credentials for the Rendered.ai Platform.'
'email:' example@rendered.ai
'password:' ***************
>>> channels = ana.get_channels()
>>> graphs = ana.get_staged_graphs()
>>> datasets = ana.get_datasets()
```

<br />

## Install the `anatools` Package
#### (Optional) Create a new Conda Environment
1. Install conda for your operating system: https://www.anaconda.com/products/individual.
2. Create a new conda environment and activate it.
3. Install anatools from the Python Package Index.

```sh
$ conda create -n renderedai python=3.7
$ conda activate renderedai
```

#### Install AnaTools to the Python Environment
1. Install AnaTools from the Python Package Index.

```sh
$ pip install anatools
```

#### Dependencies
The anatools package requires python 3.6 or higher and has dependencies on the following packages:

| Package | Description |
|-|-|
| docker | A python library for the Docker Engine API. |
| numpy | A python library used for array-based processing. |
| pillow | A fork of the Python Image Library. |
| pyyaml | A python YAML parser and emitter. |
| requests | A simple HTTP python library. |

If you have any questions or comments, contact Rendered.AI at info@rendered.ai.

<br />

## Quickstart Guide
#### What is the Rendered.ai Platform?
The Rendered.ai Platform is a synthetic dataset generation tool where graphs describe what and how synthetic datasets are generated.

| Terms | Definitions |
|-|-|
| workspace | A workspace is a collection of data used for a particular use-case, for example workspaces can be used to organize data for different projects.
| dataset | A dataset is a collection of data, for many use-cases these are images with text-based annotation files. |
| graph | A graph is defined by nodes and links, it describes the what and the how a dataset is generated. |
| node | A node can be described as an executable block of code, it has inputs and runs some algorithm to generate outputs. |
| link | A link is used to transfer data from the output of one node, to the input of other nodes. |
| channel | A channel is a collection of nodes, it is used to limit the scope of what is possible to generate in a dataset (like content from a tv channel). |

#### How do you use the SDK?
The Rendered.ai Platform creates synthetic datasets by processing a graph, so we will need to create the client to connect to the Platform API, create a graph, then create a dataset.

1. Execute the python command line, create a client and login to Rendered.ai.
In this example we are instantiating a client with no workspace or environment variables, so it is setting our default workspace.
To access the tool, you will need to use your email and password for https://deckard.rendered.ai.
```python
>>> import anatools
>>> ana = anatools.client()
'Enter your credentials for the Rendered.ai Platform.'
'email:' example@rendered.ai
'password:' ***************
```

2. Create a graph file called `graph.yml` with the code below. 
We are defining a simplistic graph for this example with multiple children's toys dropped into a container.
While `YAML` files are used in channel development and for this example, the Platform SDK and API only support `JSON`. Ensure that the `YAML` file is valid in order for the SDK to convert `YAML` to `JSON` for you. Otherwise,  provide a graph in `JSON` format. 
```yaml
version: 2
nodes:

  Rubik's Cube:
    nodeClass: "Rubik's Cube"

  Mix Cube:
    nodeClass: Mix Cube

  Bubbles:
    nodeClass: Bubbles

  Yoyo:
    nodeClass: Yo-yo

  Skateboard:
    nodeClass: Skateboard

  MouldingClay:
     nodeClass: Playdough

  ColorToys:
    nodeClass: ColorVariation
    values: {Color: "<random>"}
    links:
      Generators:
        - {sourceNode: Bubbles, outputPort: Bubbles Bottle Generator}
        - {sourceNode: Yoyo, outputPort: Yoyo Generator}
        - {sourceNode: MouldingClay, outputPort: Play Dough Generator}
        - {sourceNode: Skateboard, outputPort: Skateboard Generator}

  ObjectPlacement:
    nodeClass: RandomPlacement
    values: {Number of Objects: 20}
    links:
      Object Generators:
      - {sourceNode: ColorToys, outputPort: Generator}
      - {sourceNode: "Rubik's Cube", outputPort: "Rubik's Cube Generator"}
      - {sourceNode: Mix Cube, outputPort: Mixed Cube Generator}

  Container:
    nodeClass: Container
    values: {Container Type: "Light Wooden Box"}

  Floor:
    nodeClass: Floor
    values: {Floor Type: "Granite"}

  DropObjects:
    nodeClass: DropObjectsNode
    links:
      Objects:
        - {sourceNode: ObjectPlacement, outputPort: Objects}
      Container Generator:
        - {sourceNode: Container, outputPort: Container Generator}
      Floor Generator:
        - {sourceNode: Floor, outputPort: Floor Generator}

  Render:
    nodeClass: RenderNode
    links:
      Objects of Interest:
      - {sourceNode: DropObjects, outputPort: Objects of Interest}
```

3. Create a graph using the client.
To create a new graph, we load the graph defined above into a python dictionary using the yaml python package.
Then we create a graph using the client. This graph is being named `testgraph` and is using the `example` channel. We will first find the `channelId` matching to the `example` channel and use that in the `create_staged_graph` call. 
The client will return a `graphId` so we can reference this graph later.
```python
>>> import yaml
>>> with open('graph.yml') as graphfile:
>>>     graph = yaml.safe_load(graphfile)
>>> channels = ana.get_channels()
>>> channelId = list(filter(lambda channel: channel['name'] == 'example', channels))[0]['channelId']
>>> graphId = ana.create_staged_graph(name='testgraph', channelId=channelId, graph=graph)
>>> print(graphId)
'010f9362-daa8-4c10-a3e8-1e81e0f2e4f4'
```

4. Create a dataset using the client.
Using the `graphId`, we can create a new job to generate a dataset. The job takes some time to run.

The client will return a `datasetId` that can be used for reference later. You can use this `datasetId` to check the job status and, once the job is complete, download the dataset. You have now generated Synthetic Data!

``` python
>>> datasetId = ana.create_dataset(name='testdataset',graphId=graphId,interpretations='10',priority='1',seed='1',description='A simple dataset with cubes in a container.')
>>> datasetId
'ce66e81c-23a6-11eb-adc1-0242ac120002'
```