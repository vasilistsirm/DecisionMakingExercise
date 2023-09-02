This repo includes my code to an assignment on Decision Making using Python. I took data from last.fm and answered the assignment's questions to the corresponding .py files.
Some parts are excluded (API keys, IP adress to connect to a database) so that I protect my privacy. 

# DecisionMakingExercise
Τα ερωτήματα α, β βρίσκονται στην main.py.

Για το α,β συνδέομαι αρχικά στην βάση και έπειτα φτιάχνω τα tables(users, bands, discs). Στο users table εισάγω τυχαία στοιχεία για 20 users, στο bands/discs εισάγω
στοιχεία από το last.fm. Στο bands table έχω επιλέξει ο κάθε user να έχει το πολύ 2 αγαπημένες/ους bands/artists. Στο discs table έχω επιλέξει ο κάθε user να έχει το πολύ 1 δίσκο από την αγαπημένη του μπάντα
(ή και 1 δίσκο απο την 2η αγαπημένη του). Το παραπάνω το κάνω με σκοπό την γρηγορότερη εκτέλεση του προγράμματος και την εισαγωγή λιγότερων στοιχείων στους πίνακες.

Για τα 3 παρακάτω ερωτήματα χρησιμοποίσα την sqlalchemy για την σύνδεση στην βάση διότι παρουσίαζε warning(πρόβλημα συμβατότητας pandas και connector).

Το γ ερώτημα βρίσκεται στο αρχείο data_handling.py.

Το δ ερώτημα βρίσκεται στο αρχείο statistics.py.

Το ε ερώτημα βρίσκεται στο αρχείο data_visualization.py.

Για το ερώτημα ε τα συμπεράσματα διαφέρουν σε κάθε διαφορετική εκτέλεση του main.py και data_visualization.py διότι αλλάζουν τα στοιχεία στον πίνακα. Γενικά μπορούμε να πούμε ότι για το Distribution 
of Band Names βλέπουμε πόσες φορές εμφανίστηκε το όνομα μίας/ενός μπάντας/καλλιτέχνη δηλαδή πόσοι users έχουν αγαπημένο ένα band. Για το Distribution of Disc Names βλέπουμε πόσες φορές εμφανίζεται ένας δίσκος,
δηλαδή πόσοι users διαθέτουν αυτόν τον δίσκο. Τέλος για το Distribution of Disc Prices βλέπουμε πως κυμαίνονται οι τιμές για τους δίσκους των users.

Τα στ, ζ ερώτημα βρίσκονται στο αρχείο time_series_decomp_analysis.py.

Το ερώτημα η βρίσκεται στο αρχείο community_graph_analysis.py και χρησιμοποίησα το community_graph = nx.barabasi_albert_graph(20, 3) που δόθηκε μαζί με τα tables users,discs για να προτείνω dics που δεν έχουν
στους users.

Το ερώτημα θ βρίσκεται στο αρχείο genetic_algorithm.py





Απαλλακτική Εργασία:

Fish Swarm Algorithm Optimization του ερωτήματος θ.(Αντί για γεννετικό αλγόριθμο χρησιμοποίησα έναν αλγόριθμο σμήνους ψαριών και τον σύγκρινα με μία random όπως και στην εργασία)
Ο κώδικας για την απαλλακτική βρίσκεται στο afs_algorithm.py. (Αν αργεί πάρα πολύ να εκτελεστεί μπορείτε να αλλάξετε το num_iterations=100 σε 20 αν και θα βγάλει χειρότερα
αποτελέσματα).
