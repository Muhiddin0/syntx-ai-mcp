# Bu yerda rasimdan video generate qilish uchun apilarni ketmaketligini yozib chiqdim

Men faqatgina rasimdan video generate qilish uchun ishlatilingan API larni berib boraman. Ularni mantiqiy birlashtirish kerak bo'ladi

### Video genete qilish uchun rasim

curl 'https://api.syntx.ai/api/v1/chats/upload-files' \
 -H 'sec-ch-ua-platform: "Linux"' \
 -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo4NDc1ODE3MTIwLCJpYXQiOjE3Nzc4ODg0NTUsImV4cCI6MTc4MDQ4MDQ1NX0.95Cjh*ehUX75aj8I7wNUmwjrxvytECkcrcwwQ_4Y3dE' \
 -H 'Referer: https://syntx.ai/' \
 -H 'Accept-Language: ru' \
 -H 'sec-ch-ua: "Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"' \
 -H 'sec-ch-ua-mobile: ?0' \
 -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36' \
 -H 'Accept: application/json, text/plain, */\_' \
 -H 'Content-Type: multipart/form-data; boundary=----WebKitFormBoundarya7AfV1tqOeqt3VDO' \
 --data-raw $'------WebKitFormBoundarya7AfV1tqOeqt3VDO\r\nContent-Disposition: form-data; name="files"; filename="photo_2025-11-14_12-07-16.jpg"\r\nContent-Type: image/jpeg\r\n\r\n\r\n------WebKitFormBoundarya7AfV1tqOeqt3VDO\r\nContent-Disposition: form-data; name="check_duplicates"\r\n\r\ntrue\r\n------WebKitFormBoundarya7AfV1tqOeqt3VDO--\r\n'
response:{
"files": [
{
"filename": "photo_2025-11-14_12-07-16.jpg",
"url": "https://r2.syntx.ai/user_8475817120/uploaded/d962a34c3ebf6b05fb65880347bb3d20_b17403a1-8274-4766-b1ac-4cccd696a9b3.jpg",
"status": "success",
"content_type": "image/jpeg",
"size": 33216,
"hash": "d962a34c3ebf6b05fb65880347bb3d20",
"path": "user_8475817120/uploaded/d962a34c3ebf6b05fb65880347bb3d20_b17403a1-8274-4766-b1ac-4cccd696a9b3.jpg",
"uuid": "b17403a1-8274-4766-b1ac-4cccd696a9b3",
"preview": {
"100": "https://r2.syntx.ai/user_8475817120/uploaded/d962a34c3ebf6b05fb65880347bb3d20_b17403a1-8274-4766-b1ac-4cccd696a9b3_100.jpg",
"250": "https://r2.syntx.ai/user_8475817120/uploaded/d962a34c3ebf6b05fb65880347bb3d20_b17403a1-8274-4766-b1ac-4cccd696a9b3_250.jpg",
"500": "https://r2.syntx.ai/user_8475817120/uploaded/d962a34c3ebf6b05fb65880347bb3d20_b17403a1-8274-4766-b1ac-4cccd696a9b3_500.jpg"
}
}
],
"total": 1,
"successful": 1,
"failed": 0,
"duplicates": 0
}

### Rasimni video formatida qirib olib serverga jo'natish uchun

curl 'https://api.syntx.ai/api/v1/chats/upload-files' \
 -H 'sec-ch-ua-platform: "Linux"' \
 -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo4NDc1ODE3MTIwLCJpYXQiOjE3Nzc4ODg0NTUsImV4cCI6MTc4MDQ4MDQ1NX0.95Cjh*ehUX75aj8I7wNUmwjrxvytECkcrcwwQ_4Y3dE' \
 -H 'Referer: https://syntx.ai/' \
 -H 'Accept-Language: ru' \
 -H 'sec-ch-ua: "Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"' \
 -H 'sec-ch-ua-mobile: ?0' \
 -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36' \
 -H 'Accept: application/json, text/plain, */\_' \
 -H 'Content-Type: multipart/form-data; boundary=----WebKitFormBoundary9uEsdyKO3N0HscrR' \
 --data-raw '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'
Response:{
"files": [
{
"filename": "image-1778036155594.jpeg",
"url": "https://r2.syntx.ai/user_8475817120/hidden/5ace7dc899c27389d1ffdfc0a98aec68_ecdf31be-d5a3-48ef-b728-c57a9ed76bb8.jpeg",
"status": "duplicate",
"content_type": "image/jpeg",
"size": 14601,
"hash": "5ace7dc899c27389d1ffdfc0a98aec68",
"preview": {
"100": "https://r2.syntx.ai/user_8475817120/hidden/5ace7dc899c27389d1ffdfc0a98aec68_ecdf31be-d5a3-48ef-b728-c57a9ed76bb8_100.jpg",
"250": "https://r2.syntx.ai/user_8475817120/hidden/5ace7dc899c27389d1ffdfc0a98aec68_ecdf31be-d5a3-48ef-b728-c57a9ed76bb8_250.jpg",
"500": "https://r2.syntx.ai/user_8475817120/hidden/5ace7dc899c27389d1ffdfc0a98aec68_ecdf31be-d5a3-48ef-b728-c57a9ed76bb8_500.jpg"
}
}
],
"total": 1,
"successful": 0,
"failed": 0,
"duplicates": 1
}
Bu API succesful: 1 bo'lmaguncha yuborilan. Menimcha rasimni bo'lib bo'lib yuboradi

### Yangi chat ochildi.

curl 'https://api.syntx.ai/api/v1/chats' \
 -H 'sec-ch-ua-platform: "Linux"' \
 -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo4NDc1ODE3MTIwLCJpYXQiOjE3Nzc4ODg0NTUsImV4cCI6MTc4MDQ4MDQ1NX0.95Cjh*ehUX75aj8I7wNUmwjrxvytECkcrcwwQ_4Y3dE' \
 -H 'Referer: https://syntx.ai/' \
 -H 'Accept-Language: ru' \
 -H 'sec-ch-ua: "Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"' \
 -H 'sec-ch-ua-mobile: ?0' \
 -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36' \
 -H 'Accept: application/json, text/plain, */\_' \
 -H 'Content-Type: application/json' \
 --data-raw '{"title":"Новый чат","scope":"video"}'
response: {
"id": 11223411,
"created_at": "2026-05-06T03:08:20.085141Z",
"title": "Новый чат",
"updated_at": "2026-05-06T03:08:20.085141Z",
"owner_id": 8475817120,
"uuid": "c392111a-9065-41a7-9723-318ad81dc538",
"deleted": false,
"scope": "video",
"is_favorite": false,
"folder_uuids": [],
"messages": [],
"message_count": 0,
"message_limit": 800
}

### Ochilgan chatda video genete qilish uchun api

curl 'https://api.syntx.ai/api/v1/video/generate?ai_name=veo3' \
 -H 'sec-ch-ua-platform: "Linux"' \
 -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo4NDc1ODE3MTIwLCJpYXQiOjE3Nzc4ODg0NTUsImV4cCI6MTc4MDQ4MDQ1NX0.95Cjh*ehUX75aj8I7wNUmwjrxvytECkcrcwwQ_4Y3dE' \
 -H 'Referer: https://syntx.ai/' \
 -H 'Accept-Language: ru' \
 -H 'sec-ch-ua: "Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"' \
 -H 'sec-ch-ua-mobile: ?0' \
 -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36' \
 -H 'Accept: application/json, text/plain, */\_' \
 -H 'Content-Type: application/json' \
 --data-raw '{"chat_id":"c392111a-9065-41a7-9723-318ad81dc538","prompt":"Animate this logo","settings":{"model_type":"veo3fast_r","aspect_ratio":"16:9","type":"image","video_duration":8,"upscale":0,"image_urls":["https://r2.syntx.ai/user_8475817120/hidden/feee64b50581612d767f384a59ee62e3_6b6fafa6-48af-4f10-af32-307b60cd04b4.jpeg"]}}'
response:{
"id": 164627821,
"created_at": "2026-05-06T03:08:20.846664Z",
"chat_id": 11223411,
"author_id": 8475817120,
"updated_at": "2026-05-06T03:08:20.846664Z",
"is_favorite": null,
"message_object": [
{
"id": 256260030,
"message_id": 164627821,
"object_type": "text",
"object_url": "",
"object_text": "Animate this logo",
"completed": true,
"created_at": "2026-05-06T03:08:20.846664Z",
"updated_at": "2026-05-06T03:08:20.846664Z",
"model_type": "veo3fast_r",
"task_id": "6ad07a97-6611-4aee-9f4a-b60039469188",
"metadata": {
"width": null,
"height": null,
"aspect_ratio": null,
"payload": {
"prompt": "Animate this logo",
"chat_id": "c392111a-9065-41a7-9723-318ad81dc538",
"settings": {
"seed": null,
"type": "image",
"upscale": 0,
"mask_url": null,
"image_urls": [
"https://r2.syntx.ai/user_8475817120/hidden/feee64b50581612d767f384a59ee62e3_6b6fafa6-48af-4f10-af32-307b60cd04b4.jpeg"
],
"model_type": "veo3fast_r",
"aspect_ratio": "16:9",
"task_to_edit": null,
"video_duration": 8
},
"prompt_original": null
},
"settings": null,
"preview_url": null,
"original_url": null,
"original_urls": null,
"r2_url": null,
"r2_urls": null,
"preview_urls": null,
"all_urls": null,
"has_preview": null,
"preview": null,
"preview_size": null,
"task_id": null,
"status": null,
"error_message": null,
"duration": null,
"size": null,
"image_size": null,
"num_files": null,
"file_index": null,
"image_index": null,
"total_images": null,
"seed": null,
"enhanced_prompt": null,
"has_lyrics": null,
"lyrics": null,
"lyrics_source": null,
"lyrics_truncated": null,
"title": null,
"style": null,
"model_type": null,
"converted_from": null,
"resized_from": null,
"model": null,
"enabled_tools": null,
"default_models": null,
"use_chat_history": null,
"adding_files": null,
"files_upload_failed": null,
"vector_store_id": null,
"vector_store_status": null,
"files_completed": null,
"files_total": null,
"has_warnings": null,
"files_failed": null,
"file_id": null
}
},
{
"id": 256260031,
"message_id": 164627821,
"object_type": "image",
"object_url": "https://r2.syntx.ai/user_8475817120/hidden/feee64b50581612d767f384a59ee62e3_6b6fafa6-48af-4f10-af32-307b60cd04b4.jpeg",
"object_text": "",
"completed": true,
"created_at": "2026-05-06T03:08:20.846664Z",
"updated_at": "2026-05-06T03:08:20.846664Z",
"model_type": "veo3fast_r",
"metadata": {
"width": null,
"height": null,
"aspect_ratio": null,
"payload": {
"prompt": "Animate this logo",
"chat_id": "c392111a-9065-41a7-9723-318ad81dc538",
"settings": {
"seed": null,
"type": "image",
"upscale": 0,
"mask_url": null,
"image_urls": [
"https://r2.syntx.ai/user_8475817120/hidden/feee64b50581612d767f384a59ee62e3_6b6fafa6-48af-4f10-af32-307b60cd04b4.jpeg"
],
"model_type": "veo3fast_r",
"aspect_ratio": "16:9",
"task_to_edit": null,
"video_duration": 8
},
"prompt_original": null
},
"settings": null,
"preview_url": null,
"original_url": null,
"original_urls": null,
"r2_url": null,
"r2_urls": null,
"preview_urls": null,
"all_urls": null,
"has_preview": null,
"preview": null,
"preview_size": null,
"task_id": null,
"status": null,
"error_message": null,
"duration": null,
"size": null,
"image_size": null,
"num_files": null,
"file_index": null,
"image_index": null,
"total_images": null,
"seed": null,
"enhanced_prompt": null,
"has_lyrics": null,
"lyrics": null,
"lyrics_source": null,
"lyrics_truncated": null,
"title": null,
"style": null,
"model_type": null,
"converted_from": null,
"resized_from": null,
"model": null,
"enabled_tools": null,
"default_models": null,
"use_chat_history": null,
"adding_files": null,
"files_upload_failed": null,
"vector_store_id": null,
"vector_store_status": null,
"files_completed": null,
"files_total": null,
"has_warnings": null,
"files_failed": null,
"file_id": null
}
}
]
}

Rasim formatlari 16:9 va 9:16 bo'ladi

### Progressni tekshirish

curl 'https://api.syntx.ai/api/v1/chats/c392111a-9065-41a7-9723-318ad81dc538/inprogress' \
 -H 'sec-ch-ua-platform: "Linux"' \
 -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo4NDc1ODE3MTIwLCJpYXQiOjE3Nzc4ODg0NTUsImV4cCI6MTc4MDQ4MDQ1NX0.95Cjh*ehUX75aj8I7wNUmwjrxvytECkcrcwwQ_4Y3dE' \
 -H 'Referer: https://syntx.ai/' \
 -H 'Accept-Language: ru' \
 -H 'sec-ch-ua: "Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"' \
 -H 'sec-ch-ua-mobile: ?0' \
 -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36' \
 -H 'Accept: application/json, text/plain, */\_'
response:[
{
"message_id": 164627823,
"message_object_id": 256260033,
"object_type": "video",
"model_type": "veo3fast_r",
"created_at": "2026-05-06T03:08:20.955885+00:00",
"task_id": null
}
]
video generate qilib bo'lsa bo'sh array qaytaradi: []

### Tayyor bo'lgan video

curl 'https://api.syntx.ai/api/v1/chats/c392111a-9065-41a7-9723-318ad81dc538/164627823' \
 -H 'sec-ch-ua-platform: "Linux"' \
 -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo4NDc1ODE3MTIwLCJpYXQiOjE3Nzc4ODg0NTUsImV4cCI6MTc4MDQ4MDQ1NX0.95Cjh*ehUX75aj8I7wNUmwjrxvytECkcrcwwQ_4Y3dE' \
 -H 'Referer: https://syntx.ai/' \
 -H 'Accept-Language: ru' \
 -H 'sec-ch-ua: "Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"' \
 -H 'sec-ch-ua-mobile: ?0' \
 -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36' \
 -H 'Accept: application/json, text/plain, */\_'
Response:{
"id": 164627823,
"created_at": "2026-05-06T03:08:20.955885Z",
"chat_id": 11223411,
"author_id": -1,
"updated_at": "2026-05-06T03:08:20.955885Z",
"is_favorite": false,
"message_object": [
{
"id": 256260033,
"message_id": 164627823,
"object_type": "video",
"object_url": "https://r2.syntx.ai/user_8475817120/generated/d8878b052bfdd6fedad7a17cce076d80_9c969c95-715a-4d46-aa8c-9d0fd9ba0b1e.mp4",
"object_text": "",
"completed": true,
"created_at": "2026-05-06T03:08:20.955885Z",
"updated_at": "2026-05-06T03:09:33.092965Z",
"model_type": "veo3fast_r",
"metadata": {
"width": null,
"height": null,
"aspect_ratio": null,
"payload": {
"prompt": "Animate this logo",
"chat_id": "c392111a-9065-41a7-9723-318ad81dc538",
"settings": {
"seed": null,
"type": "image",
"upscale": 0,
"mask_url": null,
"image_urls": [
"https://r2.syntx.ai/user_8475817120/hidden/feee64b50581612d767f384a59ee62e3_6b6fafa6-48af-4f10-af32-307b60cd04b4.jpeg"
],
"model_type": "veo3fast_r",
"aspect_ratio": "16:9",
"task_to_edit": null,
"video_duration": 8
},
"prompt_original": null
},
"settings": null,
"preview_url": "https://r2.syntx.ai/user_8475817120/thumbnails/video_thumb_5182cb29-f672-454e-98e4-a8756f8854f6.jpg",
"original_url": "https://r2.syntx.ai/veo3/dolphin/2026/05/06/13137699_1778036963.mp4",
"original_urls": null,
"r2_url": null,
"r2_urls": null,
"preview_urls": null,
"all_urls": null,
"has_preview": null,
"preview": null,
"preview_size": null,
"task_id": 256260033,
"status": null,
"error_message": null,
"duration": 8.0,
"size": null,
"image_size": null,
"num_files": null,
"file_index": null,
"image_index": null,
"total_images": null,
"seed": null,
"enhanced_prompt": null,
"has_lyrics": null,
"lyrics": null,
"lyrics_source": null,
"lyrics_truncated": null,
"title": null,
"style": null,
"model_type": null,
"converted_from": null,
"resized_from": null,
"model": null,
"enabled_tools": null,
"default_models": null,
"use_chat_history": null,
"adding_files": null,
"files_upload_failed": null,
"vector_store_id": null,
"vector_store_status": null,
"files_completed": null,
"files_total": null,
"has_warnings": null,
"files_failed": null,
"file_id": null
}
}
]
}
