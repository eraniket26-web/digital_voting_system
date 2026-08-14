from flask import Flask, jsonify

app = Flask(__name__)

voting_dictonary = {
             "candidates" : { }
            }

@app.route('/')
def context() :
    return jsonify({'msg':'Welcome to the App'}),200

@app.route('/health')
def healthCheck() :
    return jsonify({'msg':'App is running'}),200


@app.route('/vote/<string:name>',methods=['POST'])
def logVote(name) :

  # Verify name should not be empty 
   if not name.strip():
       return jsonify({
            'error': 'Candidate name cannot be empty.'
        }), 400
   
   existing_names = []
   count = 0
   # Step 1 :- Collect the existing name from collection
   if not voting_dictonary['candidates']:
       print('Candidates are not present')
   else :
     for candidate_id , candidate_data in voting_dictonary['candidates'].items():
         existing_names.append(candidate_data['name'])   

   # Step 2 :- Check if name is present in existing list     
   if name not in existing_names:
       add_vote = {'name': name, 'vote': 1}
       count = len(voting_dictonary['candidates']) + 1
       voting_dictonary['candidates'][f'c{count}'] = add_vote
    #    print('candidate added')
   else:      
    #    print(f'printing values', voting_dictonary.items())
       for candidate_id , candidate_data in voting_dictonary['candidates'].items():
           if(candidate_data['name'] == name) :
               vote = candidate_data['vote'] + 1
               voting_dictonary['candidates'][candidate_id]['vote'] = vote
               break

  
#    print(f'Exisitng names in list', existing_names)
   return jsonify ({'msg': "Your vote has been successfully recorded."}), 200


@app.route('/results')
def displayResults():
    return voting_dictonary

@app.route('/reset')
def resetVotes() :
    voting_dictonary.clear()
    return jsonify({'msg': 'Votes record reset successfully'}), 200


if __name__ == '__main__':
    app.run(debug=True)