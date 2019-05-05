   ## Strava API
   This application finds duplicated cyclist in Istanbul and calculate a score for each rider listed in those segments.

   <b>Built with</b>
    - [Python3.7](https://www.python.org)
    - [Django 2.2](https://www.djangoproject.com)
    - [Django REST Framework](http://www.django-rest-framework.org)
    
   ## Installation
   ```
   pipenv install
   ```   
   
   ## Definition of variables and formula

   **Endpoint 1:**
    Find the most popular 10 cycling segments in Istanbul, and check their leaderboards (First 50). 
    Return a dictionary of riders only in multiple leaderboards, and how many time they are listed in those leaderboards. (Endpoint 1)
    
   **Endpoint 2:**
   Calculate a score for each rider listed in those segments and return your highscore list. (Endpoint 2) 
   
   **Calculation**
   
        - avg_speed:        The average riding speed for all the distance travelled
                            within the given boundaries. If riders too slow or too fast
                            it's impact their score
        - avg_elev_diff:    The average of the segments's elevation difference
        - count:            This displays the how many time they are listed in those leaderboards
        - rank:             Contains all the rank that riders won Example: [3,5,10,1]
        - rank_score:       If the rider's rank in certain range, rider gets extra points

        formula: (avg_speed * avg_elev_diff * rank_score * count) / 1000
    
   