# The "Memory Flash" Algorithm

**Goal**: decrease the amount of time it takes the user to produce the correct answer to a given question.

The algorithm is built around completing "sessions" of studying. A session is a set of cards that the user will review until their response time decreases below the median `TimeToAnswer` for all cards in the session (more on this later). A session has two stages: [*aquire*](#aquire) and [*speed up*](#speed-up).

## Aquire

### Unseen Cards

This stage simply puts unseen cards from the deck into the session. If all cards in the deck have been seen, skip to [Seen Cards](#seen-cards).
	
	keep showing user unseen cards and adding them to the Session while (
		number_of_unseen_cards in session < 8 
		or sum_of_time_to_answer for cards in session < 60 seconds
		or no unseen cards left in deck
	)
	then, add seen cards to the session

Why use a 8 card minimum? [Because the average person can only hold 7 different chunks of information in working memory](https://en.wikipedia.org/wiki/Working_memory#Capacity). In order to speed up recall, the Memory Flash algorithm attempts to stress the user's memory enough that they do not instantly recall subsequent reviews of the same card. 

The 60 second minimum is designed to ensure that if the questions in the deck can be answered quickly, there will be enough questions that the *Speed Up* stage is still difficult.

### Seen Cards

If this is the first time that the deck has been reviewed, skip to the [Speed Up](#speed-up) stage.

Along with unseen cards, we also want to speed up recall on cards that the user has already seen; especially cards that the user previously took longer to recall.

To pick the flashcards that need to be reviewed the most, the algorithm chooses flashcards based on a [weighted random selection](http://peterkellyonline.blogspot.com/2012/02/weighted-random-selection-in-php.html) (WRS) of `TimeToAnswer` values for all flashcards in the deck (that have been seen previously). `TimeToAnswer` is a measure of how long it takes the user to answer the flashcard correctly. But, there is one small twist that the algorithm uses when selecting `TimeToAnswer` from the database for WRS. Instead of selecting the `TimeToAnswer` of the most recent review, the query will select the `TimeToAnswer` of the first review on the last day the flashcard was reviewed.

-- write about priming --

```
if unseen cards still left in deck (
	num_seen_cards_to_add_to_deck = num_cards_in_session * (1/3)
	add num_seen_cards_to_add_to_deck to the Session using weighted ...
		random selection based on TimeToAnswer
) else if no unseen cards left in deck (
	add cards to session using weighted random selection while (
		sum_of_time_to_answer for cards in session < 60 seconds
	)
)
```

The next section explains why the factor 1/3 was used above.

## Speed Up

The goal of this algorithm is to "decrease the amount of time it takes the user to produce the correct answer to a given question." A corollary to the this goal, and the implementation, is that the `TimeToAnswer` of the flashcards will move toward equalization. This stage consists of practicing the flashcards until each flashcard's `TimeToAnswer` is below the median from when the session moved from the *Aquire* stage to the *Speed Up* stage. AND, first_attempt_correct is true for all cards. 

-- explain 1/3 --

Why the median? Because the median is the middle point, it is reasonable to assume that all the flashcards above the median are capabale of being answered  in less than the `TimeToAnswer` of the original median of the session. After all the flashcards are below this median, a new Session is started and this process is repeated.