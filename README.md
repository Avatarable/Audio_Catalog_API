# Audio_Catalog_API
A Flask Web API that simulates the behavior of an audio file server while using SQL database

 Available audio types: Songs, Podcasts, & Audiobooks

GET or POST an audio type: .../audios/<string:audioType>
GET or UPDATE or DELETE a particular audio: .../audios/<string:audioType>/<int:id>


Examples:

GET all songs:
.../audios/songs

Add a podcasts:
.../audios/podcasts

DELETE a particular audiobook:
.../audios/audiobooks/2
