PostgreSQL account: cl4335
URL: http://35.231.10.166:8111/home
Description: We implemented all the features mentioned in part 1 (except for register type). Users can input whatever information they want provided on the website to query course and professor info. Also user can login to their student account and check their status as well as the course they registered for. The register type is abandoned due to it being forgotten during implementing part 2 and part 3.

The two interesting webpages are "search" and "professor" where we allow users to query desired target by filtering with all the conditions provided on the webpage. Our backend loads the input and include only the valid (nonempty) conditions and add them to the query. Giving such liberty to users might result in difficulties while using our system since we open all the options to the users, with unrealistic conditions, the result is doomed to be NULL.

