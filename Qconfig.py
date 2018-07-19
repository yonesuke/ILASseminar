# Before you can use the jobs API, you need to set up an access token.
# Log in to the Quantum Experience. Under "Account", generate a personal 
# access token. Replace "None" below with the quoted token string.
# Uncomment the APItoken variable, and you will be ready to go.

APItoken = "e59359d7d79d74905edd7667e7ab717f505f0291fa2f46a7f69d8a778476188698a52701111acf2859e63ee9d3cbd28149c2680722714e9f5a20dd92d76476ab"

config = {
  "url": 'https://quantumexperience.ng.bluemix.net/api'
}

if 'APItoken' not in locals():
  raise Exception("Please set up your access token. See Qconfig.py.")
