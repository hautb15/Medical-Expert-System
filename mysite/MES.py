### CHƯƠNG TRÌNH HỖ TRỢ CHẨN ĐOÁN BỆNH DỰA TRÊN LUẬT DẪN ###
# Import các module và khởi tạo biến
from pyknow import *
import pandas as pd
import io

diseases_list = []
diseases_symptoms = []
symptom_map = {}
d_desc_map = {}
d_treatment_map = {}

# Đọc dữ liệu
data = pd.read_csv('disease-symptoms.csv', encoding='utf-8',index_col=0)

# Đọc file tương tác với Front-End
in_f_FE = open('home\\data\input.txt',encoding='utf-8')
FE_s_data = in_f_FE.read()
s_FE = FE_s_data.split("\n")
s_FE.pop()
in_f_FE.close()

symptom_f = open('symptoms.txt',encoding='utf-8')
symptom_data = symptom_f.read()
s_symptom = symptom_data.split("\n")
symptom_f.close()

df_FE = pd.DataFrame()
df_FE['name'] = s_symptom
df_FE['value'] = s_FE

# khai báo các hàm
def preprocess():
	global diseases_list,diseases_symptoms,symptom_map,d_desc_map,d_treatment_map
	diseases_list = list(data.iloc[:0,2:])

	for disease in diseases_list:
		disease_s_file = open("Disease-symptoms\\" + disease + ".txt",encoding='utf-8')
		disease_s_data = disease_s_file.read()
		s_list = disease_s_data.split("\n")
		symptom_map[str(s_list)] = disease
		disease_s_file.close()
		
		disease_s_file = open("Disease-descriptions\\" + disease + ".txt",encoding='utf-8')
		disease_s_data = disease_s_file.read()
		d_desc_map[disease] = disease_s_data
		disease_s_file.close()
		disease_s_file = open("Disease-treatments\\" + disease + ".txt",encoding='utf-8')
		disease_s_data = disease_s_file.read()
		d_treatment_map[disease] = disease_s_data
		disease_s_file.close()
		#print(diseases_list,type(diseases_list)) # type list
		#print(symptom_map,type(symptom_map)) # type dict {[yes,no,..]: disease}
		#print(d_desc_map,type(d_desc_map)) # dict, this is description
		#print(d_treatment_map,type(d_treatment_map))
		# print(s_list, type(s_list))
		# print(disease, type(disease))

def identify_disease(*arguments):
	symptom_list = []
	for symptom in arguments:
		symptom_list.append(symptom)
	# Handle key error
	return symptom_map[str(symptom_list)]

def get_details(disease):
	return d_desc_map[disease]

def get_treatments(disease):
	return d_treatment_map[disease]

def if_not_matched(disease):
		print("")
		id_disease = disease
		disease_details = get_details(id_disease)
		treatments = get_treatments(id_disease)		
		# print("")
		# print("CÓ KHẢ NĂNG BẠN ĐANG MẮC PHẢI CĂN BỆNH: %s\n" %(id_disease))
		# print("DƯỚI ĐÂY LÀ MÔ TẢ NGẮN VỀ CĂN BỆNH NÀY :\n")
		# print(disease_details+"\n")		
		# print("CÁC LOẠI THUỐC VÀ PHÁC ĐỒ ĐIỀU TRỊ THEO Ý KIẾN BÁC SĨ LÀ: \n")
		# print(treatments+"\n")
		
		lines = ['VỚI TRIỆU CHỨNG CỦA BẠN, KHÔNG CÓ CHÍNH XÁC BẤT KỲ LOẠI BỆNH NÀO TRONG DỮ LIỆU CỦA HỆ THỐNG, TUY NHIÊN BẠN CÓ THỂ MẮC PHẢI BỆNH: ']
		lines.append(id_disease)
		lines.append('\n\nDƯỚI ĐÂY LÀ MÔ TẢ NGẮN VỀ CĂN BỆNH NÀY :\n')
		lines.append(disease_details)
		lines.append('\n\nCÁC LOẠI THUỐC VÀ PHÁC ĐỒ ĐIỀU TRỊ THEO Ý KIẾN BÁC SĨ LÀ: \n')
		lines.append(treatments)

		with open('home\\data\output.txt', 'a',encoding='utf-8') as f:
			f.truncate(0)
			f.writelines(lines)
			f.close()

class Greetings(KnowledgeEngine):
	@DefFacts()
	def _initial_action(self):
		print("")
		print("XIN CHÀO! ĐÂY LÀ HỆ THỐNG HỖ TRỢ CHẨN ĐOÁN BỆNH, CHÚNG TÔI RẤT HÂN HẠNH PHỤC VỤ BẠN.")
		print("VÌ VẬY CHÚNG TÔI CẦN BẠN CUNG CẤP MỘT SỐ THÔNG TIN VỀ TÌNH TRẠNG SỨC KHỎE CỦA MÌNH ")
		print("BẠN CÓ CẢM THẤY BẤT KỲ TRIỆU CHỨNG NÀO SAU ĐÂY KHÔNG?:")
		print("")
		yield Fact(action="find_disease")


	@Rule(Fact(action='find_disease'), NOT(Fact(headache=W())),salience = 1)
	def symptom_0(self):
		self.declare(Fact(headache=df_FE.iloc[0,1]))

	@Rule(Fact(action='find_disease'), NOT(Fact(cough=W())),salience = 1)
	def symptom_1(self):
		self.declare(Fact(cough=df_FE.iloc[1,1]))

	@Rule(Fact(action='find_disease'), NOT(Fact(eruptive=W())),salience = 1)
	def symptom_2(self):
		self.declare(Fact(eruptive=df_FE.iloc[2,1]))

	@Rule(Fact(action='find_disease'), NOT(Fact(rhinorrhea=W())),salience = 1)
	def symptom_3(self):
		self.declare(Fact(rhinorrhea=df_FE.iloc[3,1]))

	@Rule(Fact(action='find_disease'), NOT(Fact(red_eyes=W())),salience = 1)
	def symptom_4(self):
		self.declare(Fact(red_eyes=df_FE.iloc[4,1]))

	@Rule(Fact(action='find_disease'), NOT(Fact(psomophagia=W())),salience = 1)
	def symptom_5(self):
		self.declare(Fact(psomophagia=df_FE.iloc[5,1]))
	 
	@Rule(Fact(action='find_disease'), NOT(Fact(sore_throat=W())),salience = 1)
	def symptom_6(self):
		self.declare(Fact(sore_throat=df_FE.iloc[6,1]))
	
	@Rule(Fact(action='find_disease'), NOT(Fact(fever=W())),salience = 1)
	def symptom_7(self):
		self.declare(Fact(fever=df_FE.iloc[7,1]))
	
	@Rule(Fact(action='find_disease'), NOT(Fact(glandulae_parotis=W())),salience = 1)
	def symptom_8(self):
		self.declare(Fact(glandulae_parotis=df_FE.iloc[8,1]))
	
	@Rule(Fact(action='find_disease'), NOT(Fact(deradenoncus=W())),salience = 1)
	def symptom_9(self):
		self.declare(Fact(deradenoncus=df_FE.iloc[9,1]))
	
	@Rule(Fact(action='find_disease'), NOT(Fact(arthralgia=W())),salience = 1)
	def symptom_10(self):
		self.declare(Fact(arthralgia=df_FE.iloc[10,1]))

	@Rule(Fact(action='find_disease'), NOT(Fact(erythematous_syphilid=W())),salience = 1)
	def symptom_11(self):
		self.declare(Fact(erythematous_syphilid=df_FE.iloc[11,1]))

	@Rule(Fact(action='find_disease'), NOT(Fact(bulla=W())),salience = 1)
	def symptom_12(self):
		self.declare(Fact(bulla=df_FE.iloc[12,1]))

	@Rule(Fact(action='find_disease'), NOT(Fact(blood_dots=W())),salience = 1)
	def symptom_13(self):
		self.declare(Fact(blood_dots=df_FE.iloc[13,1]))

	@Rule(Fact(action='find_disease'),Fact(headache="no"),Fact(cough="yes"),Fact(eruptive="yes"),Fact(rhinorrhea="yes"),Fact(red_eyes="yes"),\
		Fact(psomophagia="no"),Fact(sore_throat="no"),Fact(fever="yes"),	Fact(glandulae_parotis="no"),Fact(deradenoncus="no"),Fact(arthralgia="no"),\
			Fact(erythematous_syphilid="no"),Fact(bulla="no"),Fact(blood_dots="no"))
	def disease_0(self):
		self.declare(Fact(disease="Soi"))

	@Rule(Fact(action='find_disease'),Fact(headache="no"),Fact(cough="no"),Fact(eruptive="no"),Fact(rhinorrhea="no"),Fact(red_eyes="no"),\
		Fact(psomophagia="yes"),Fact(sore_throat="no"),Fact(fever="yes"),Fact(glandulae_parotis="yes"),Fact(deradenoncus="no"),Fact(arthralgia="yes"),\
			Fact(erythematous_syphilid="no"),Fact(bulla="no"),Fact(blood_dots="no"))
	def disease_1(self):
		self.declare(Fact(disease="QuaiBi"))

	@Rule(Fact(action='find_disease'),Fact(headache="no"),Fact(cough="no"),Fact(eruptive="yes"),Fact(rhinorrhea="no"),Fact(red_eyes="no"),\
		Fact(psomophagia="no"),Fact(sore_throat="no"),Fact(fever="yes"),Fact(glandulae_parotis="no"),Fact(deradenoncus="yes"),Fact(arthralgia="yes"),\
			Fact(erythematous_syphilid="no"),Fact(bulla="no"),Fact(blood_dots="no"))
	def disease_2(self):
		self.declare(Fact(disease="Rubella"))

	@Rule(Fact(action='find_disease'),Fact(headache="yes"),Fact(cough="no"),Fact(eruptive="no"),Fact(rhinorrhea="no"),Fact(red_eyes="no"),\
		Fact(psomophagia="no"),Fact(sore_throat="yes"),Fact(fever="yes"),Fact(glandulae_parotis="no"),Fact(deradenoncus="no"),Fact(arthralgia="no"),\
			Fact(erythematous_syphilid="yes"),Fact(bulla="yes"),Fact(blood_dots="no"))
	def disease_3(self):
		self.declare(Fact(disease="ThuyDau"))

	@Rule(Fact(action='find_disease'),Fact(headache="yes"),Fact(cough="no"),Fact(eruptive="no"),Fact(rhinorrhea="no"),Fact(red_eyes="no"),\
		Fact(psomophagia="no"),Fact(sore_throat="no"),Fact(fever="yes"),Fact(glandulae_parotis="no"),Fact(deradenoncus="no"),Fact(arthralgia="yes"),\
			Fact(erythematous_syphilid="no"),Fact(bulla="no"),Fact(blood_dots="yes"))
	def disease_4(self):
		self.declare(Fact(disease="SotXuatHuyet"))


	@Rule(Fact(action='find_disease'),Fact(disease=MATCH.disease),salience = -998)
	def disease(self, disease):
		print("")	
		id_disease = disease
		disease_details = get_details(id_disease)
		treatments = get_treatments(id_disease)
		print("")
		print("KHẢ NĂNG CAO BẠN ĐANG MẮC PHẢI CĂN BỆNH %s\n" %(id_disease))
		print("DƯỚI ĐÂY LÀ MÔ TẢ NGẮN VỀ CĂN BỆNH NÀY :\n")
		print(disease_details+"\n")		
		print("CÁC LOẠI THUỐC VÀ QUY TRÌNH ĐIỀU TRỊ BỞI BÁC SĨ LÀ: \n")
		print(treatments+"\n")

		lines = ['CÓ KHẢ NĂNG BẠN ĐANG MẮC PHẢI CĂN BỆNH: ']
		lines.append(id_disease)
		lines.append('\n\nDƯỚI ĐÂY LÀ MÔ TẢ NGẮN VỀ CĂN BỆNH NÀY :\n')
		lines.append(disease_details)
		lines.append('\n\nCÁC LOẠI THUỐC VÀ PHÁC ĐỒ ĐIỀU TRỊ THEO Ý KIẾN BÁC SĨ LÀ: \n')
		lines.append(treatments)

		with open('home\\data\output.txt', 'a',encoding='utf-8') as f:
			f.truncate(0)
			f.writelines(lines)
			f.close()

	@Rule(Fact(action='find_disease'),
		  Fact(headache=MATCH.headache),
		  Fact(cough=MATCH.cough),
		  Fact(eruptive=MATCH.eruptive),
		  Fact(rhinorrhea=MATCH.rhinorrhea),
		  Fact(red_eyes=MATCH.red_eyes),
		  Fact(psomophagia=MATCH.psomophagia),
		  Fact(sore_throat=MATCH.sore_throat),
		  Fact(fever=MATCH.fever),
		  Fact(glandulae_parotis=MATCH.glandulae_parotis),
		  Fact(deradenoncus=MATCH.deradenoncus),
		  Fact(arthralgia=MATCH.arthralgia),
		  Fact(erythematous_syphilid=MATCH.erythematous_syphilid),
		  Fact(bulla=MATCH.bulla),
		  Fact(blood_dots=MATCH.blood_dots),NOT(Fact(disease=MATCH.disease)),salience = -999)

	def not_matched(self,headache,cough,eruptive,rhinorrhea,red_eyes,psomophagia,sore_throat,fever,glandulae_parotis,\
		deradenoncus,arthralgia,erythematous_syphilid,bulla,blood_dots):
		print("\nVỚI TRIỆU CHỨNG CỦA BẠN, KHÔNG CÓ CHÍNH XÁC BẤT KỲ LOẠI BỆNH NÀO TRONG CSDL CỦA HỆ THỐNG, TUY NHIÊN BẠN CÓ THỂ: ")
		lis = [headache,cough,eruptive,rhinorrhea,red_eyes,psomophagia,sore_throat,fever,glandulae_parotis,\
		deradenoncus,arthralgia,erythematous_syphilid,bulla,blood_dots]
		max_count = 0
		max_disease = ""
		for key,val in symptom_map.items():
			count = 0
			temp_list = eval(key)
			for j in range(0,len(lis)):
				if(temp_list[j] == lis[j] and lis[j] == "yes"):
					count = count + 1
			if count > max_count:
				max_count = count
				max_disease = val
		if max_count >= 1:
			if_not_matched(max_disease)
		elif max_count == 0:
			print('\nBẠN KHÔNG MẮC BẤT KỲ CĂN BỆNH NÀO TRONG NHÓM BỆNH CÓ SẴN CỦA HỆ THỐNG!\n')
			lines = ['BẠN KHÔNG MẮC BẤT KỲ CĂN BỆNH NÀO TRONG NHÓM BỆNH CÓ SẴN CỦA HỆ THỐNG!']
			with open('home\\data\output.txt', 'a',encoding='utf-8') as f:
				f.truncate(0)
				f.writelines(lines)
				f.close()		
		

# Thực thi
if __name__ == "__main__":
	preprocess()
	engine = Greetings()

	engine.reset()  # Prepare the engine for the execution.
	engine.run()  # Run it!
	print(engine.facts)
	# while(1):
	# 	engine.reset()  # Prepare the engine for the execution.
	# 	engine.run()  # Run it!
	# 	print("BẠN CÓ MUỐN TIẾP TỤC CHẨN ĐOÁN BÊNH KHÔNG?")
	# 	if input() == "no":
	# 		break
	# 	print(engine.facts)
