import sys, string, os
import struct,time,hashlib,urllib2,urllib

user_id=1114
app_id=20100
app_secret='a1a337326a5c40e99c413e4116315733'
base_url='http://shcboxplatform.shopyourway.com'
debug_mode=False


def discover(limit=100):
	offline_token=get_offline_token(user_id,app_id)
	debug_it("Offline Token: " + offline_token)
	hash = hashlib.sha256(offline_token+app_secret).hexdigest()
	product_ids_strings = call_endpoint("/products/discover", offline_token, hash, {'maxItems':limit})
	comma_seperated_ids = product_ids_strings[1:-1]
	products_details = call_endpoint("/products/get", offline_token, hash, {'ids':comma_seperated_ids, 'with':'tags'})
	return products_details


def get_products_by_tags(tag_ids):
	offline_token=get_offline_token(user_id,app_id)
	debug_it("Offline Token: " + offline_token)
	hash = hashlib.sha256(offline_token+app_secret).hexdigest()
	new_tag_ids = remove_black_listed_tags(tag_ids)
	comma_seperated_tag_ids = str(new_tag_ids)[1:-1]
	products_details = call_endpoint("/products/get-by-tags", offline_token, hash, {'tagIds':comma_seperated_tag_ids, 'with':'tags'})
	return products_details

def remove_black_listed_tags(tag_ids):
	tags_to_exclude = [414208,479499,479516,5601110,3923331,4125531,5066939,1776576,1962220,5969363,5031419,4785512,1098204,1098227,1112005,1173137,1245774,1324787,1324813,1611877,760011,760034,760038,760024,760057,760012,760013,760059,760063,760021,760067,760054,760001,760074,760027,760007,760053,760055,760010,760051,760006,760071,760018,760015,760069,760019,760023,760066,760008,760016,760040,760005,760050,760056,760070,760052,760047,760002,760041,760035,760022,760028,760033,760060,760075,760044,760046,760032,760065,760061,760003,760064,760025,760072,760058,760062,760037,760030,760045,760029,760020,760026,760073,760043,760031,760009,760068,760036,760049,760039,760017,760048,760004,760042,224510,221554,479499]
	new_tags_list = [x for x in tag_ids if x not in tags_to_exclude]
	return new_tags_list

######  below you can find methods for internal usage ######



#################################################################################
# This method makes the call to the platform-api, 				  				#
#################################################################################
def call_endpoint(endpoint, token, hash, params):
	path = base_url + endpoint + "?"
	params['token'] = str(token)
	params['hash'] = str(hash)
	req_param=urllib.urlencode(params.items())
	debug_it("## platform-call: " + path + req_param)
	pageEndpoint=urllib2.urlopen(path,req_param,timeout=5)
	results=pageEndpoint.read()
	return results



#################################################################################
# This method returns the signiture needed for getting the Offline Access Token #
#################################################################################
def get_signature(user_id,app_id,time_stamp,app_secret):
	userid_buffer=buffer(struct.pack('@q', user_id),0)
	appid_buffer=buffer(struct.pack('@q', app_id),0)
	timestamp_buffer=buffer(struct.pack('@d',time_stamp),0)
	appsecret_buffer=buffer(bytearray(ord(app_secret[i]) for i in range(0,len(app_secret))),0)
	new_hash=hashlib.sha256()
	new_hash.update(str(userid_buffer)+str(appid_buffer)+str(timestamp_buffer)+str(appsecret_buffer))
	signature=new_hash.hexdigest()
	return signature

#################################################################################
# This method returns the token needed for creating the hash                    #
#################################################################################
def get_offline_token(user_id,appid_prod):
	uxtime=int(time.time())
	signature=get_signature(user_id,app_id,uxtime,app_secret)
	time_stamp_str=time.strftime("%Y-%m-%d %H:%M:%S",time.gmtime(uxtime)).replace(' ','T')
	req_url=base_url+'/auth/get-token?'
	req_param=urllib.urlencode([('userId',str(user_id)),('appId',str(appid_prod)),('timestamp',time_stamp_str),('signature',signature)])
	debug_it("url:" + req_url)
	debug_it("params:" + req_param)
	page=urllib2.urlopen(req_url,req_param,timeout=5)
	token=page.read().replace('"','')
	return token

def debug_it(text):
	if debug_mode==True: 
		print text



## Scripting \ Main
if __name__ == "__main__":
	import sys
	debug_mode=True
	print discover()
	print remove_black_listed_tags([414208, 414209])
	print get_products_by_tags([414208, 414209])
	exit(0)

