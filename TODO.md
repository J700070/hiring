# Done
- [x] Project setup and installation
- [x] Backend mock inspection algorithm
- [x] New model for inspection results
- [x] Return inspection results from backend on endpoint call
- [x] Frontend display of inspection results in a simple way
- [x] Improve frontend UI for the dashboard


# TODO
- [ ] Add tests to the backend and frontend
- [ ] Review dependencies to check for security vulnerabilities and unused packages
- [ ] Further improvements in the frontend UI and UX
-> Dashboard should provide a better overview of the inspection results. Show more info about the inspection results in the frontend dashboard (e.g. type of anomalies, confidence, time taken to run the algorithm, etc.)
-> Dashboard should be easier to understand at a glance. Use charts and graphs to display the inspection results in a more visual way
-> There should be a clear design language and a consistent look and feel across the application. I've assummed the default dark theme for Elastic UI, but this should be improved and documented.
-> Depending on the use case I would rethink the choice of ElasticUI and consider other headless UI libraries for better UX and flexibility.
- [ ] Add early filters to the inspection algorithm to avoid running it on images that are not likely to pass
- [ ] Add pre-processing to the images before running the inspection algorithm to ensure the best results
- [ ] Better logging and error handling in the backend
- [ ] Add authentication and authorization to the backend
- [ ] Many design choices (like the anomalies model) were made based on assumptions. I would discuss these with the team to ensure they are the best fit for the use case.
- [ ] Depending on the use case, SEO and accessibility should be considered
- [ ] An analytics tool should also be added to the frontend to track user interactions and improve the application based on the data
