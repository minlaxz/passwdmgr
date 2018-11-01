# passwdmgr by laxz
<h2> Password Manager </h2>
<p>Tdy , we have to remember many email and password combination to log in many sites (domains)</p>
<pre>This password manager Python Client is for storing password and email of many domains. 
This demo will store encoded password and encoded email on firebase realtime database
(0) You can check your password and email for a specific site (domain).
(1) If there is no domain record in database, this will prompt you to enter email and password.
(2) If you enter email and password , and there is no domain record also , this will encode all
sensitive data and submit to firebase.
(3) If there is domain record in firebase database, this will grap all data from firebase and
decode to readable data and monitor for user.
(4) OK well, other error handlings ..., THANKS
(caution!) This is for personal use only , There must not have 2 domain with same name, means>>
One Domain One Account (Personal).
(TODO(0)) You need to have your serviceKey.json file to access your firebase database.
(TODO(1))In my case , I already have from firebase console. "Quick search" >> <a href="https://firebase.google.com/docs/database/admin/start?authuser=0">"Firebase admin"></a>
</pre>

<sub> Thanks by laxz </sub>
