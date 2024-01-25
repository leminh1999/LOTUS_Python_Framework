# <<< VERSION: 1.1 >>>
# PC2 chạy từ các task1 sau khi đến thời gian chuyển đổi đề bắt link từ tác vụ 1 và lần lượt vào check nội dung comment và cập nhật mySQL về điểm Funny.
# Nếu điểm Funny thỏa thì nó sẽ thả Tim và follow kênh đó.
#
# 	- Tất cả các máy chạy Task1 sẽ được chuyển nhiệm vụ qua Task2 tại thời điểm cài đặt trước trong bảng Config.
# 	Ví dụ: Tại thời điểm 6h sáng mỗi ngày thì các máy Task1 sẽ được chuyển qua Task2 để check comment.
# 	- Khi 1 máy nào đó check hết dòng được check thì nó sẽ bật cờ task2_running_flag trong bảng config lên và tự chuyển sang Task1 trở lại.
# 	- Trạng thái hoạt động của các NV sẽ được cập nhật tại bảng NVStatus.
#
# Table config:
#   + post_every_x_day: <số ngày>
#   + last_post_date: <thời gian>
#   + switch_task2_time: <thời gian trong ngày theo phút>
#
# Table  task_mon
#   + task1_running_flag: <cờ báo task1 đang chạy>
#   + task2_running_flag: <cờ báo task2 đang chạy>
#
# Các bước thực hiện:
# 	Máy kiểm tra trạng thái cờ đang mở:
# 	  + Khi cờ task1_running_flag được bật lên: máy cần kiểm tra ngày hiện tại của hệ thống trừ đi ngày của lần post trước (last_post_date) có lớn hơn thời gian tối đa cho 1 lần xuất bản hay không (post_every_x_day) và thời gian hiện tại có đang vượt quá thời gian chuyển đổi task1 thành task 2 hay chưa (switch_task2_time). Nếu nhỏ hơn thì tiếp tục. Nếu lớn hơn thì cập nhật mySQL để đổi trạng thái cờ lại là task1_running_flag = 0 và task2_running_flag = 1.
# 	  + Khi cờ task2_running_flag được bật lên: mỗi lần chạy 1 tour. Máy sẽ kiểm tra còn dòng nào có nội dung task2_check_time là -999 nữa không? Nếu còn thì chạy tiếp. Nếu hết rồi thì cập nhật task1_running_flag = 1 và task2_running_flag = 0.
#
# 	Nếu là task2_running_flag = 1 thì thực hiện các bước sau:
# 	3. Load mẫu thông tin mẫu video từ mySQL:
# 		+ Lấy video có thời gian cập nhật là -999.
#     + Kiểm tra xem còn video vậy không. Nếu không còn thì cập nhật cờ task2_running_flag = 0 và cập nhật task1_running_flag = 1.
# 	4. Truy cập video clip.
# 		a. Cập nhật lại điểm Like, Comment, Share.
# 		b. Đếm điểm cười.
# 		c. Chụp hình nội dung comment nếu điểm cười lớn hơn điểm cười tối thiểu.
# 		d. Nếu đạt tiêu chuẩn cười mà kênh chưa được follow thì nhấn follow
# 	5. Cập nhật lại thông tin và điểm số lên mySQL.
# 	Điền vào cột giờ kiểm tra task2_check_time. Theo kiểu sau:
# 		○ Đây là cột record thời gian theo giờ mà Task2 đã kiểm tra theo số phút lấy từ thời điểm 0h0min.
# 		VD: task 2 check comment lúc 2h30 phút thì giá trị cột này là 2*60+30 = 150
# 		○ Giá trị mặc định của ô này là -999 khi ô mới khởi tạo. Vậy:
# Lặp lại vô tận từ bước 3 đến bước 5.
#
#=======================================================================================
### Điều kiện chạy ###
# 1. Tỉ lệ màn hình 1920x1080
# 2. Vị trí chrome và của sổ code như hình. Images/9b.png
# 3. Cửa sổ chrome mặc định mở lên là maximize
# 3. Tỉ lệ màn hình Web là 1350x947 (phần còn lại của code) Images/8b.png
#    Mở phần xem code rồi click giữ cạnh biên để resize. Khi resize sẽ xuất hiện con số để canh tỉ lệ.
#=======================================================================================

# from B2_GetComment_ImportList import *

# task2GetComment = Task2GetComment





