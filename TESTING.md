TESTING
=======

Who: List of people on the team
-----------
* Andrew Lim
* Ryan Matthews
* Juan Carlos Herrera
* John Murphy
* Charlie Luckhart

Title: of project
-----------
* Better Beer

Vision: from Project Part 1 Proposal
-----------
* Vision Statement: "The perfect beer for you"
* Motivation: We want good beer

Automated Tests: Testing scraper and MySQL Database
-----------
### Test 1 - Scraper
* To test the scraper first you need to have BeauitfulSoup4. Change into the data-retrival directory and type in 'python beerScript.py "beer brand"'. You will be prompted to input a number corresponding to the beers listed. After inputing the desired beer number, the bitterness level as well as the alcohol by volume will appear on the screen.
* ![Scraper Test Screenshot](scraper-test-results.png?raw=true)

### Test 2 - MySQL
* To test our MySQL database we used a [mysqltest](https://dev.mysql.com/doc/mysqltest/2.0/en/mysqltest.html). We used a simple sample test case (test_mysql in our home directory) in order to check the integrity of our MySQL data. We are using this just to test if MySQL is working properly on our server.
* ![MySQL Test Screenshot](mysql-test-results.png?raw=true)


User Acceptance Tests: Copy of at least three UAT plans
-----------
* ![User Test Case: 1](1.png?raw=true)
* ![User Test Case: 2](2.png?raw=true)
* ![User Test Case: 3](3.png?raw=true)
