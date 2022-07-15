# API Design

## RESTful interfaces

Formally:

* Client-server based architecture
* Stateless - all information related to a particular request
  should be contained in the request itself.
* Cachability - yes/no
* Layered system - Client shouldn't be aware if they're connected
  to the final server, of if there's an intermediate server.
* Uniform interface, without prerequisites.
  - Resource identification in requests,
  - Resource manipulation through representation,
  - Self-descriptive messages
  - Hypermedia as the engine of application state
* Code on demand

Colloquially:

* Usually understood as interfaces based on HTTP resources using JSON formatted requests.
* URIs should describe clear resources as well as HTTP methods and actions to perform
  on them, following CRUD (Create, Retrieve, Update, Delete)
