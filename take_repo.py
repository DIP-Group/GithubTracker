import pickle

# Step 2
with open('repo.pkl', 'rb') as config_dictionary_file:
 
    # Step 3
    repo = pickle.load(config_dictionary_file)
 
    # After config_dictionary is read from file
    issues = repo.get_issues()

    for issue in issues:
        print(issue)