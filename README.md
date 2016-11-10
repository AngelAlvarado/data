# Table of Contents

0. [How to use this code](README.md#how-to-use)
1. [My notes about requirements](README.md#understanding-requirements)
2. [Basic UML of features](README.md#basic-uml)
5. [Details of implementation so far](README.md#details-of-my-own-implementation)
6. [Sketches](README.md#sketches)
7. [Personal notes](README.md#personal-notes)

## How to use

@todo create a docker container to provide python 3.5 , pip, pandas, numexpr
@warning this is a Beta version. Dependencies/requirements could change and will be documented in this README file.

From root folder run as: $ ./run.sh ./paymo_input/batch_payment.csv ./paymo_input/stream_payment.csv ./paymo_output/output1.txt ./paymo_output/output2.txt ./paymo_output/output3.txt

Or from ./insight_testsuite execute ./run_test.sh

#### Requirements

```
------------------
python: 3.5.1.final.0
pandas: 0.18.0
numexpr: 2.4.4

```

#### Log

@see ./results.txt file for events while analyzing payments and/or preparing batch data.

## Understanding requirements
My Notes about requirements:

* Datasets: The Dataset is 'real'-Venmo. If the dataset has interesting data, use it for new features. batch_payment.csv (old transactions) - use to build the initial state of the user network. stream_payment.csv (stream transactions?) - use it to detect fraud or warn user.

** id1: ID of user making the payment
** id2: ID of user receiving the payment

* Verify stream_payment.csv and batch_payment.csv have content. Using: $ cat file | more. Yes it has emojis, lol.

* Input: No need to connect to an API. Datasets are inside paymo_input directory.

* Output: Process each line from stream_payment.csv and for each payment output a line containing TRUSTED or UNVERIFIED.

* Assume that stream_payment.csv corresponds to new payments - design program to handle text file with large number of payments.

* Of course we want this to be fast -> It's critical that these features don't take too long to run.

* Well-documented and scalable code

* Write unit-tests especially because data is not clean

* Use Python

* Use a private repo in Github (taking advantage of my private repos)

* Top directory must have paymo_input and paymo_output directories and a script called run.sh that compiles and runs the program that implements the features.

* Pass arguments to my own run.sh and run.sh will pass arguments to python script.

* Directory structure will be verified

###Feature 1

<img src="./requirements/uml/feature1.png" width="500">

###Feature 2

<img src="./requirements/friend-of-a-friend1.png" width="500">
<img src="./requirements/uml/feature2.png" width="500">

###Feature 3

<img src="./requirements/fourth-degree-friends2.png" width="600">
<img src="./requirements/uml/feature3.png" width="500">

##Basic UML
Basic UML sequence diagrams created via PlantUML in order to make them version-able.
@see ./requirements/uml/*.puml

##Details of my own implementation

#### Clean (Sanitize) batch data 

* run.sh will take care of cleaning the first batch of data (batch_payment.csv). I'll need only id1 and id2 so far.

#### Goal in my code

My implementation is based on Python 3. This solution requires pandas and numexpr libraries.

The dataframes and numexpr solution is not optimal to calculate 2nd, 3rd and 4th-degree friends. It will be very slow.
An optimal solution will be to use an adjacency matrix theorem: https://people.math.osu.edu/husen.1/teaching/sp2003/571/graphs.pdf.

The goal is to create a matrix with the following structure: (@see sketch [3](./requirements/sketches/sketch3_20161106_032115.jpg) top-left corner).

            UserA   UserB  UserC
    UserA    0       0      0
    UserB    1       0      1
    UserC    1       0      0

Then multiple this matrix by itself up to 3 times to generate a matrix with 4th-degree friends. For example: 

            UserA   UserB  UserC
    UserA    0       2      0
    UserB    1       0      3
    UserC    1       0      2
    
(@see sketch [3](./requirements/sketches/sketch1_20161106_032036.jpg top-right corner)).

* **Warning:** If there's a new payment with new users I'll need to regenerate the matrices, which might take a while. 
* An optimal solution will be to use some graph theory and linear algebra. 

####  Sketches

While this did seem like a simple challenge at the beginning, I struggled and had to go over and over my ideas. Here are some important sketches.

<img src="./requirements/sketches/sketch1_20161106_032036.jpg" width="500">

<img src="./requirements/sketches/sketch2_20161106_032110.jpg" width="500">

<img src="./requirements/sketches/sketch3_20161106_032115.jpg" width="500">

##Testing

Execute ./insight_testsuite/run_tests.sh

#Personal notes

* *Notify only when not a friend of a friend or when friend of a friend hasn’t made transactions? Re: Only if there were transactions before.*

* *While processing new payment the network could grow, right? Yes*

* *Let’s say we don’t have the network on cache?*

* *I’ll document features in the README file. I’m using python 2.7 and pandas - maybe pandas is not needed.*

* *If I need libraries, environments or dependencies I have to document them in the README file*

* *UNIT test. For example: Date in payments greater or equal than current date always in new payments*

* *Data could be in the wrong format. E.G. Two commas for strings! - I’ll clean data before Python reads it.*

* *Create a separate table per person?*

* *Clean integers in IDs and put them into a error file*

* *Dependencies: python 3.5, “conda”, pip3.5, conda install numexpr -> dataframe.query*

* *What if while in a transaction the process is exited/terminated*

* *I was thinking on using dictionaries but decided to use dataframes very heavily*

* *Maybe I need to clean id1 and id2 -> clean the commas?*

* *There are users with id 0 which I guess is fine*

## References

## Feature ideas
