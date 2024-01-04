# Project "Bulletin Board"

This project is something like an Internet resource bulletin board for a fan server of a well-known MMORPG and is implemented on the Django framework.

Users of this resource have the opportunity to register in it by e-mail, receiving a letter with a registration confirmation code. After registration, they can create and edit advertisements.
(Registration is available by clicking on the "***Registration***" button on the start page. The registration form implemented at "http://127.0.0.1:8000/sign/signup/" is not yet working!)

Unauthorized users can only view advertisements in a general list and in detail. When viewing a list, pagination is used.

Ads consist of a title and text, which may contain pictures, embedded videos from youtube.com and other content. The WYSIWYG editor CK-editor is used to format text, attach pictures and videos.

Users can post plain text responses to other users' advertisements. When sending a response, the user receives an e-mail notifying about it. The user also has access to a private page with responses to his ads, inside which he can filter responses by ad, delete them and accept them (when a response is accepted, a notification is also sent to the user who left the response). In addition, when creating an advertisement, the user defines it in one of the following categories: Tanks, Healers, DDs, Merchants, Guildmasters, Questgivers, Blacksmiths, Tanners, Potions Masters, Spell Masters.
