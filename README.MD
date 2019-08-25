After having trouble setting up Braintree subscription service for my site, I wanted to share a getting started guide.
This is a minimum viable app wreitten with Django 2.0 but the python methods can be transfered to any framework.
<ul>
  <li>
  Register a user
  </li>
  <li>
  cancell subscription
  </li><li>
  change payment method on file
  </li><li>
  change password
  </li><li>
  email lost password
  </li>
  </ul>
  
Getting started Steps:<br>
<ol>
  <li>
Create a virtual environment.</lu><br>
`python3 venv env`<br><li>
Install dependancies<br>
`pip install -r requirements.txt`</lu>
<li>
Copy and paste your: <br>
BT_ENVIRONMENT,
BT_MERCHANT_ID,
BT_PUBLIC_KEY,
BT_PRIVATE_KEY,
  </lu><br>
PLAN_ID Vlaues into lines 132-136 in the setting file to be able to make test transactions.</lu><li>
Fill out lines 140-146 to be able to send emails.</lu>
