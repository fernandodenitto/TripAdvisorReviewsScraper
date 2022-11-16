import requests
import json
from bs4 import BeautifulSoup 
import math,time # compute number of pages and reviews
import random # as above
from utils import *
import pandas as pd
import re

print('\033[92m') #Just a green screen color
print("\n-----    Welcome to SpotAdvisorScraper   -----\n(Remember to visit first TripAdvisor with your Chrome Browser)")
input("Press ENTER to continue...")

print("Getting Cookies and Parameters from your Chrome Browser...")
#Getting cookies from Chrome
cookies=getCookiesFromDomain('tripadvisor')
TASID=getCookiesFromDomain('tripadvisor','TASID')
CSRF=getCookiesFromDomain('tripadvisor','roybatty') # For avoid XS Forgery (you need to access in chrome before to execute this file otherwirse it will return null)
print("Parameters Ready!")


name_dataset=input("How you want to call the Dataset File (.csv) ?\t")


print("Getting all the spots from file spots_link.txt ...")

#listings = []

filename=input("From which file (that contains links of spots) do you want to scrape data? ")

# with open(filename) as file:
#     for line in file:
#         listings.append(line.rstrip())

# print("Done!")

# For optimize the application is better to manage the big files (more than 500 links) splitting the overall listing in sublists and iterate over theme
# In particulare create a new and empty dataset and store in a file called Review_bla_bla_part_X
# For this reason it was define in the file utility.py the below function
spot_groups=split_file_by_lines(filename,500)



# ----- This part of code refers to get all the reviews for each spot ----- #

#URL for the graphql call in tripadvisor
GRAPHQL_URL = 'https://www.tripadvisor.com/data/graphql/batched'

#Useful function for get ids of the place from the URL
def get_ids_from_spot_url(url):
  url = url.split('-')
  geo = url[1]
  loc = url[2]
  return (int(geo[1:]), int(loc[1:]))

# Function for request content from graphql
def request_graphql(url, page=0):
  geo, loc = get_ids_from_spot_url(url)
  request = [
      {
          "query": "mutation LogBBMLInteraction($interaction: ClientInteractionOpaqueInput!) {\n  logProductInteraction(interaction: $interaction)\n}\n",
          "variables": {
              "interaction": {
                  "productInteraction": {
                      "interaction_type": "CLICK",
                      "site": {
                          "site_name": "ta",
                          "site_business_unit": "Hotels",
                          "site_domain": "www.tripadvisor.com"
                      },
                      "pageview": {
                          "pageview_request_uid": "X@2fPQokGCIABGTeHYoAAAES",
                          "pageview_attributes": {
                              "location_id": loc,
                              "geo_id": geo,
                              "servlet_name": "Hotel_Review"
                          }
                      },
                      "user": {
                          "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Safari/537.36",
                          "site_persistent_user_uid": "web373a.83.56.0.34.17609EB3BAC",
                          "unique_user_identifiers": {
                              "session_id": 'TASID=C5D15569548141648AF979F61B69DED5; Domain=www.tripadvisor.com; Expires=Sun, 31-Oct-2021 11:08:38 GMT; Path=/; Secure'
                          }
                      },
                      "search": {},
                      "item_group": {
                          "item_group_collection_key": "X@2fPQokGCIABGTeHYoAAAES"
                      },
                      "item": {
                          "product_type": "Hotels",
                          "item_id_type": "ta-location-id",
                          "item_id": loc,
                          "item_attributes": {
                              "element_type": "es",
                              "action_name": "REVIEW_FILTER_LANGUAGE"
                          }
                      }
                  }
              }
          }
      },
      {
          "query": "query ReviewListQuery($locationId: Int!, $offset: Int, $limit: Int, $filters: [FilterConditionInput!], $prefs: ReviewListPrefsInput, $initialPrefs: ReviewListPrefsInput, $filterCacheKey: String, $prefsCacheKey: String, $keywordVariant: String!, $needKeywords: Boolean = true) {\n  cachedFilters: personalCache(key: $filterCacheKey)\n  cachedPrefs: personalCache(key: $prefsCacheKey)\n  locations(locationIds: [$locationId]) {\n    locationId\n    parentGeoId\n    name\n    placeType\n    reviewSummary {\n      rating\n      count\n    }\n    keywords(variant: $keywordVariant) @include(if: $needKeywords) {\n      keywords {\n        keyword\n      }\n    }\n    ... on LocationInformation {\n      parentGeoId\n    }\n    ... on LocationInformation {\n      parentGeoId\n    }\n    ... on LocationInformation {\n      name\n      currentUserOwnerStatus {\n        isValid\n      }\n    }\n    ... on LocationInformation {\n      locationId\n      currentUserOwnerStatus {\n        isValid\n      }\n    }\n    ... on LocationInformation {\n      locationId\n      parentGeoId\n      accommodationCategory\n      currentUserOwnerStatus {\n        isValid\n      }\n      url\n    }\n    reviewListPage(page: {offset: $offset, limit: $limit}, filters: $filters, prefs: $prefs, initialPrefs: $initialPrefs, filterCacheKey: $filterCacheKey, prefsCacheKey: $prefsCacheKey) {\n      totalCount\n      preferredReviewIds\n      reviews {\n        ... on Review {\n          id\n          url\n          location {\n            locationId\n            name\n          }\n          createdDate\n          publishedDate\n          provider {\n            isLocalProvider\n          }\n          userProfile {\n            id\n            userId: id\n            isMe\n            isVerified\n            displayName\n            username\n            avatar {\n              id\n              photoSizes {\n                url\n                width\n                height\n              }\n            }\n            hometown {\n              locationId\n              fallbackString\n              location {\n                locationId\n                additionalNames {\n                  long\n                }\n                name\n              }\n            }\n            contributionCounts {\n              sumAllUgc\n              helpfulVote\n            }\n            route {\n              url\n            }\n          }\n        }\n        ... on Review {\n          title\n          language\n          url\n        }\n        ... on Review {\n          language\n          translationType\n        }\n        ... on Review {\n          roomTip\n        }\n        ... on Review {\n          tripInfo {\n            stayDate\n          }\n          location {\n            placeType\n          }\n        }\n        ... on Review {\n          additionalRatings {\n            rating\n            ratingLabel\n          }\n        }\n        ... on Review {\n          tripInfo {\n            tripType\n          }\n        }\n        ... on Review {\n          language\n          translationType\n          mgmtResponse {\n            id\n            language\n            translationType\n          }\n        }\n        ... on Review {\n          text\n          publishedDate\n          username\n          connectionToSubject\n          language\n          mgmtResponse {\n            id\n            text\n            language\n            publishedDate\n            username\n            connectionToSubject\n          }\n        }\n        ... on Review {\n          id\n          locationId\n          title\n          text\n          rating\n          absoluteUrl\n          mcid\n          translationType\n          mtProviderId\n          photos {\n            id\n            statuses\n            photoSizes {\n              url\n              width\n              height\n            }\n          }\n          userProfile {\n            id\n            displayName\n            username\n          }\n        }\n        ... on Review {\n          mgmtResponse {\n            id\n          }\n          provider {\n            isLocalProvider\n          }\n        }\n        ... on Review {\n          translationType\n          location {\n            locationId\n            parentGeoId\n          }\n          provider {\n            isLocalProvider\n            isToolsProvider\n          }\n          original {\n            id\n            url\n            locationId\n            userId\n            language\n            submissionDomain\n          }\n        }\n        ... on Review {\n          locationId\n          mcid\n          attribution\n        }\n        ... on Review {\n          __typename\n          locationId\n          helpfulVotes\n          photoIds\n          route {\n            url\n          }\n          socialStatistics {\n            followCount\n            isFollowing\n            isLiked\n            isReposted\n            isSaved\n            likeCount\n            repostCount\n            tripCount\n          }\n          status\n          userId\n          userProfile {\n            id\n            displayName\n            isFollowing\n          }\n          location {\n            __typename\n            locationId\n            additionalNames {\n              normal\n              long\n              longOnlyParent\n              longParentAbbreviated\n              longOnlyParentAbbreviated\n              longParentStateAbbreviated\n              longOnlyParentStateAbbreviated\n              geo\n              abbreviated\n              abbreviatedRaw\n              abbreviatedStateTerritory\n              abbreviatedStateTerritoryRaw\n            }\n            parent {\n              locationId\n              additionalNames {\n                normal\n                long\n                longOnlyParent\n                longParentAbbreviated\n                longOnlyParentAbbreviated\n                longParentStateAbbreviated\n                longOnlyParentStateAbbreviated\n                geo\n                abbreviated\n                abbreviatedRaw\n                abbreviatedStateTerritory\n                abbreviatedStateTerritoryRaw\n              }\n            }\n          }\n        }\n        ... on Review {\n          text\n          language\n        }\n        ... on Review {\n          locationId\n          absoluteUrl\n          mcid\n          translationType\n          mtProviderId\n          originalLanguage\n          rating\n        }\n        ... on Review {\n          id\n          locationId\n          title\n          labels\n          rating\n          absoluteUrl\n          mcid\n          translationType\n          mtProviderId\n          alertStatus\n        }\n      }\n    }\n    reviewAggregations {\n      ratingCounts\n      languageCounts\n      alertStatusCount\n    }\n  }\n}\n",
          "variables": {
              "locationId": loc,
              "offset": page * 20,
              "filters": [
                #   {
                #       "axis": "LANGUAGE",
                #       "selections": [
                #           "es",
                #           "en",
                #           "de",
                #           "fr",
                #           "it"
                #       ]
                #   }
              ],
              "prefs": None,
              "initialPrefs": {},
              "limit": 20,
              "filterCacheKey": None,
              "prefsCacheKey": "locationReviewPrefs",
              "needKeywords": False,
              "keywordVariant": "location_keywords_v2_llr_order_30_en"
          }
      },
      {
          "query": "mutation UpdateReviewSettings($key: String!, $val: String!) {\n  writePersonalCache(key: $key, value: $val)\n}\n",
          "variables": {
              "key": "locationReviewFilters_4107099",
              "val": "[{\"axis\":\"LANGUAGE\",\"selections\":[\"es\"]}]"
          }
      }
  ]
  response = requests.post(GRAPHQL_URL, json=request, headers={
      'origin': 'https://www.tripadvisor.com',
      'pragma': 'no-cache',
      'referer': url,
      'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Safari/537.36',
      'x-requested-by': 'TNI1625!AJFQ0tyDV0Lu7eV93v0BOxfMYTX11LMLKmO74ng4Y0z2X8GokwW%2FtY3LkoOf6ppcuz3luweZ1A15cBGTg5fdb121RLdEzMkrhKaLua177r18IdY6myQ2WHE%2BSXyT3pAGaAKZEidOTMMkWGHRZl4k6FBQenWGusYRAzBjce2qvD%2Fs%2C1',
      'Cookie': 'TADCID=dBXKGwKW3lSZk2zdABQCFdpBzzOuRA-9xvCxaMyI12kzCTB5n5GV9J50ztj1YR8-n0FrYPejWyHVNj77fDfy7JoTJtmG13sEAu8; TAUnique=%1%enc%3AwKqxFrOQIPAiJfWlErNTlERmd2fsjtUQLXahdUfng77sw28igpq7iw%3D%3D; TASSK=enc%3AAKD%2B7NQjBu%2FC39GfCu9gacLMYcLewNvr6jJpG%2BJ7bpmgMHv1BCmc3l61WltcdzBa9naTxztyMhMzEKnbaTWTVsxpcInQfVhGiPncgzwsTYiKtf%2FoLlDDrywofo3QnTLQOQ%3D%3D; ServerPool=X; PMC=V2*MS.90*MD.20211031*LD.20211031; TART=%1%enc%3AIiX1pRKzU5SqEoRhIpO2EDngzL337Fzl%2F1gUQfC9%2BEm%2FTJaCaZd9zhcSGiha%2F1deszF3R8nmubQ%3D; TATravelInfo=V2*AY.2021*AM.12*AD.31*DY.2022*DM.1*DD.1*A.2*MG.-1*HP.2*FL.3*DSM.1635674663313*RS.1; TASID=E6C9A4011E6145459D70111828BC7849; ak_bmsc=723EAE42033532A60D68B120A395F616~000000000000000000000000000000~YAAQB+HaF23bF8p8AQAAd6vO1Q3u94mmA+ekSpZcDbOaluQg9eHd5nr2l3bLInTNAsd102iSl9j0aBHfKK8YpBzbsVxa1akF8OfeyTafeRcslpld666tn7YsqZKh8Vk1ZCQfB99qMPZjvqc2E36BlKuGo0d9Uqx4HDEaRDj49J3Qj3mvHaapgCovXEHcqn80mmgR/FIRBPeW5haGB++8PvhiI3Mt6PYI+7E23koVplY0OEYQny6OUXBUfXw+fY4REm0eT/oOt6zAbxwBQb97RfbyONkUIAHH+VzEu/ZHn8nh/BD4mNdsI78p2SszS6F4RacrUREwqTvIWIxDdB6JUcEp36UZ+teJcDWFKLTkHCOVbLwOpbUI6w/dNmUOH9DumHaTBKMvm5tthLqEXksfaA==; _evidon_consent_cookie={"consent_date":"2021-10-31T10:04:29.977Z","categories":{"7":true},"vendors":{"7":{"14":true,"17":true,"31":true,"36":true,"51":true,"56":true,"58":true,"64":true,"66":true,"80":true,"81":true,"82":true,"99":true,"103":true,"131":true,"139":true,"167":true,"168":true,"174":true,"237":true,"242":true,"243":true,"249":true,"253":true,"257":true,"259":true,"265":true,"286":true,"290":true,"292":true,"298":true,"307":true,"310":true,"321":true,"322":true,"348":true,"355":true,"364":true,"384":true,"395":true,"412":true,"433":true,"442":true,"457":true,"459":true,"464":true,"474":true,"480":true,"516":true,"529":true,"550":true,"560":true,"564":true,"606":true,"608":true,"631":true,"633":true,"635":true,"650":true,"667":true,"674":true,"735":true,"831":true,"853":true,"905":true,"920":true,"921":true,"948":true,"1028":true,"1095":true,"1256":true,"1455":true,"1635":true,"1647":true,"1812":true,"1872":true,"1879":true,"1904":true,"1955":true,"2191":true,"2253":true,"2449":true,"2516":true,"2521":true,"2609":true,"2770":true,"2937":true,"3110":true,"3173":true,"3222":true,"3437":true,"3490":true,"3568":true,"3622":true,"3794":true,"3857":true,"3952":true,"3994":true,"4100":true,"4160":true,"4166":true,"4548":true,"4668":true,"4782":true,"4902":true,"5037":true,"5129":true,"5181":true,"5205":true,"5277":true,"5431":true,"6171":true,"6423":true,"6609":true}},"cookies":{"7":true},"consent_type":1}; TATrkConsent=eyJvdXQiOiIiLCJpbiI6IkFMTCJ9; PAC=ABXDVWXj0J9E8rW-CfCCRr9RHM63KDct5xiNrIzQGUMya6ymHABmd26yzpshZCbyfcZJb0JT6bvt9_juqqRXu1OkFjVVLiulrhQJLDrDWHk8lB8H4qeUD10zjvWpdlt0br2XiQu1G_Wh_ClrMtDwXrHKJGdWTPP31dADbOKL8CkNWXi-bnqbP-cmxDQeBZ9D-IcDR4PjwMM8ZSfeho8X_AvyKmj-PXf-27-lTrbLcO5YjW8NItUeVoJc1Jwjz-EZ4YsbCrsHTFkPDFv8Int4lKmqgF8bnVoGfaxWbOQBf-eymPKJqBn1yXHW-vNYBQXC5hmoY2Tq_nHFf6yoo8LQ9mk%3D; VRMCID=%1%V1*id.10568*llp.%2FHotel_Review-g659610-d6765045-Reviews-or20-Affittacamera_B_B_Porta_Grande-Mesagne_Province_of_Brindisi_Puglia%5C.html*e.1636279758458; TAReturnTo=%1%%2FHotel_Review-g659610-d6765045-Reviews-or5-Affittacamera_B_B_Porta_Grande-Mesagne_Province_of_Brindisi_Puglia.html; roybatty=TNI1625!AJFQ0tyDV0Lu7eV93v0BOxfMYTX11LMLKmO74ng4Y0z2X8GokwW%2FtY3LkoOf6ppcuz3luweZ1A15cBGTg5fdb121RLdEzMkrhKaLua177r18IdY6myQ2WHE%2BSXyT3pAGaAKZEidOTMMkWGHRZl4k6FBQenWGusYRAzBjce2qvD%2Fs%2C1; SRT=%1%enc%3AIiX1pRKzU5SqEoRhIpO2EDngzL337Fzl%2F1gUQfC9%2BEm%2FTJaCaZd9zhcSGiha%2F1deszF3R8nmubQ%3D; TASession=V2ID.E6C9A4011E6145459D70111828BC7849*SQ.27*LS.DemandLoadAjax*GR.94*TCPAR.44*TBR.5*EXEX.15*ABTR.59*PHTB.8*FS.39*CPU.28*HS.recommended*ES.popularity*DS.5*SAS.popularity*FPS.oldFirst*LF.ALL*FA.1*DF.0*TRA.false*LD.6765045*EAU._; TAUD=LA-1635674667628-1*RDD-1-2021_10_31*HDD-928304-2021_12_31.2022_01_01.1*LD-939745-2021.12.31.2022.1.1*LG-939747-2.1.F.; bm_sv=5527CFE92BFC7E596702B0B42351D9E6~He1rYlbPTna1D+GP8Yw9gUEE0SYmeKMtBECUbPUh5CMEuAmHHzLFxq2X61H9Lyvoi12fv7IR02pSRTBtfseX2mEuBOsZJR6URRRqKrbXqaxePAGYmKOSpJo8D7nkQUkUYz4bBgssRCDd4BogYCdAK0rws0FmOixEj184Ays8QR0=; __vt=aSV5s9J7sRoqSOMXABQCIf6-ytF7QiW7ovfhqc-AvRkQxlUL0XB0TN6tXwuMsK6ol-5QAJX_p_JLc2o8cA6JkBWlauqix-Z5mqfNFB-zz8kj3pnCyaUl-HctRzGIFTkmuxqQ1Y3_-oJT7WzrAgxUOLroK7A'
  })
  return response.json()

# Same function as above with cookies and parameters in arguments
def request_graphql_with_cookies(url,cookies,TASID,CSRF,page=0,):
  # This version of the functions get all the fresh cookies and quantities given by arguments
  # For this reason you have to get them before to call it with the function getCookieFromDomain in the file webUtils
  # Another way is to use selenium to automatize the process
  geo, loc = get_ids_from_spot_url(url)
  request = [
      {
          "query": "mutation LogBBMLInteraction($interaction: ClientInteractionOpaqueInput!) {\n  logProductInteraction(interaction: $interaction)\n}\n",
          "variables": {
              "interaction": {
                  "productInteraction": {
                      "interaction_type": "CLICK",
                      "site": {
                          "site_name": "ta",
                          "site_business_unit": "Hotels",
                          "site_domain": "www.tripadvisor.com"
                      },
                      "pageview": {
                          "pageview_request_uid": "X@2fPQokGCIABGTeHYoAAAES",
                          "pageview_attributes": {
                              "location_id": loc,
                              "geo_id": geo,
                              "servlet_name": "Hotel_Review"
                          }
                      },
                      "user": {
                          "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Safari/537.36",
                          "site_persistent_user_uid": "web373a.83.56.0.34.17609EB3BAC",
                          "unique_user_identifiers": {
                              "session_id": TASID
                          }
                      },
                      "search": {},
                      "item_group": {
                          "item_group_collection_key": "X@2fPQokGCIABGTeHYoAAAES"
                      },
                      "item": {
                          "product_type": "Hotels",
                          "item_id_type": "ta-location-id",
                          "item_id": loc,
                          "item_attributes": {
                              "element_type": "es",
                              "action_name": "REVIEW_FILTER_LANGUAGE"
                          }
                      }
                  }
              }
          }
      },
      {
          "query": "query ReviewListQuery($locationId: Int!, $offset: Int, $limit: Int, $filters: [FilterConditionInput!], $prefs: ReviewListPrefsInput, $initialPrefs: ReviewListPrefsInput, $filterCacheKey: String, $prefsCacheKey: String, $keywordVariant: String!, $needKeywords: Boolean = true) {\n  cachedFilters: personalCache(key: $filterCacheKey)\n  cachedPrefs: personalCache(key: $prefsCacheKey)\n  locations(locationIds: [$locationId]) {\n    locationId\n    parentGeoId\n    name\n    placeType\n    reviewSummary {\n      rating\n      count\n    }\n    keywords(variant: $keywordVariant) @include(if: $needKeywords) {\n      keywords {\n        keyword\n      }\n    }\n    ... on LocationInformation {\n      parentGeoId\n    }\n    ... on LocationInformation {\n      parentGeoId\n    }\n    ... on LocationInformation {\n      name\n      currentUserOwnerStatus {\n        isValid\n      }\n    }\n    ... on LocationInformation {\n      locationId\n      currentUserOwnerStatus {\n        isValid\n      }\n    }\n    ... on LocationInformation {\n      locationId\n      parentGeoId\n      accommodationCategory\n      currentUserOwnerStatus {\n        isValid\n      }\n      url\n    }\n    reviewListPage(page: {offset: $offset, limit: $limit}, filters: $filters, prefs: $prefs, initialPrefs: $initialPrefs, filterCacheKey: $filterCacheKey, prefsCacheKey: $prefsCacheKey) {\n      totalCount\n      preferredReviewIds\n      reviews {\n        ... on Review {\n          id\n          url\n          location {\n            locationId\n            name\n          }\n          createdDate\n          publishedDate\n          provider {\n            isLocalProvider\n          }\n          userProfile {\n            id\n            userId: id\n            isMe\n            isVerified\n            displayName\n            username\n            avatar {\n              id\n              photoSizes {\n                url\n                width\n                height\n              }\n            }\n            hometown {\n              locationId\n              fallbackString\n              location {\n                locationId\n                additionalNames {\n                  long\n                }\n                name\n              }\n            }\n            contributionCounts {\n              sumAllUgc\n              helpfulVote\n            }\n            route {\n              url\n            }\n          }\n        }\n        ... on Review {\n          title\n          language\n          url\n        }\n        ... on Review {\n          language\n          translationType\n        }\n        ... on Review {\n          roomTip\n        }\n        ... on Review {\n          tripInfo {\n            stayDate\n          }\n          location {\n            placeType\n          }\n        }\n        ... on Review {\n          additionalRatings {\n            rating\n            ratingLabel\n          }\n        }\n        ... on Review {\n          tripInfo {\n            tripType\n          }\n        }\n        ... on Review {\n          language\n          translationType\n          mgmtResponse {\n            id\n            language\n            translationType\n          }\n        }\n        ... on Review {\n          text\n          publishedDate\n          username\n          connectionToSubject\n          language\n          mgmtResponse {\n            id\n            text\n            language\n            publishedDate\n            username\n            connectionToSubject\n          }\n        }\n        ... on Review {\n          id\n          locationId\n          title\n          text\n          rating\n          absoluteUrl\n          mcid\n          translationType\n          mtProviderId\n          photos {\n            id\n            statuses\n            photoSizes {\n              url\n              width\n              height\n            }\n          }\n          userProfile {\n            id\n            displayName\n            username\n          }\n        }\n        ... on Review {\n          mgmtResponse {\n            id\n          }\n          provider {\n            isLocalProvider\n          }\n        }\n        ... on Review {\n          translationType\n          location {\n            locationId\n            parentGeoId\n          }\n          provider {\n            isLocalProvider\n            isToolsProvider\n          }\n          original {\n            id\n            url\n            locationId\n            userId\n            language\n            submissionDomain\n          }\n        }\n        ... on Review {\n          locationId\n          mcid\n          attribution\n        }\n        ... on Review {\n          __typename\n          locationId\n          helpfulVotes\n          photoIds\n          route {\n            url\n          }\n          socialStatistics {\n            followCount\n            isFollowing\n            isLiked\n            isReposted\n            isSaved\n            likeCount\n            repostCount\n            tripCount\n          }\n          status\n          userId\n          userProfile {\n            id\n            displayName\n            isFollowing\n          }\n          location {\n            __typename\n            locationId\n            additionalNames {\n              normal\n              long\n              longOnlyParent\n              longParentAbbreviated\n              longOnlyParentAbbreviated\n              longParentStateAbbreviated\n              longOnlyParentStateAbbreviated\n              geo\n              abbreviated\n              abbreviatedRaw\n              abbreviatedStateTerritory\n              abbreviatedStateTerritoryRaw\n            }\n            parent {\n              locationId\n              additionalNames {\n                normal\n                long\n                longOnlyParent\n                longParentAbbreviated\n                longOnlyParentAbbreviated\n                longParentStateAbbreviated\n                longOnlyParentStateAbbreviated\n                geo\n                abbreviated\n                abbreviatedRaw\n                abbreviatedStateTerritory\n                abbreviatedStateTerritoryRaw\n              }\n            }\n          }\n        }\n        ... on Review {\n          text\n          language\n        }\n        ... on Review {\n          locationId\n          absoluteUrl\n          mcid\n          translationType\n          mtProviderId\n          originalLanguage\n          rating\n        }\n        ... on Review {\n          id\n          locationId\n          title\n          labels\n          rating\n          absoluteUrl\n          mcid\n          translationType\n          mtProviderId\n          alertStatus\n        }\n      }\n    }\n    reviewAggregations {\n      ratingCounts\n      languageCounts\n      alertStatusCount\n    }\n  }\n}\n",
          "variables": {
              "locationId": loc,
              "offset": page * 20,
              "filters": [
                #   {
                #       "axis": "LANGUAGE",
                #       "selections": [
                #           "es",
                #           "en",
                #           "de",
                #           "fr",
                #           "it"
                #       ]
                #   }
              ],
              "prefs": None,
              "initialPrefs": {},
              "limit": 20,
              "filterCacheKey": None,
              "prefsCacheKey": "locationReviewPrefs",
              "needKeywords": False,
              "keywordVariant": "location_keywords_v2_llr_order_30_en"
          }
      },
      {
          "query": "mutation UpdateReviewSettings($key: String!, $val: String!) {\n  writePersonalCache(key: $key, value: $val)\n}\n",
          "variables": {
              "key": "locationReviewFilters_4107099",
              "val": "[{\"axis\":\"LANGUAGE\",\"selections\":[\"es\"]}]"
          }
      }
  ]
  response = requests.post(GRAPHQL_URL, json=request, headers={
      'origin': 'https://www.tripadvisor.com',
      'pragma': 'no-cache',
      'referer': url,
      'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Safari/537.36',
      'x-requested-by': CSRF,
      'Cookie': cookies
  })
  return response.json()


#Getting the information about the Location and the number of reviews to compute the number of pages to download
# Each page (request to graphql) contain 20 review so the NUM_PAGES=TOTAL_NUM_REVIEWS/20

#Ask how many pages user want to scrape for each spot
MAX_PAGES=int(input("How many (max)pages of reviews (for each spot) do you want to scrape? (each page contains 20 reviews)\t"))
#MAX_PAGES=5 #100 reviews at max

index=1 #for count the progression

for (group_index,listings) in enumerate(spot_groups):

    print(f"SCRAPING THE GROUP N.{group_index}")

    # List where I will store all reviews
    data=[]

    for (index,spot_url) in enumerate(listings):

        try:
            response = request_graphql_with_cookies(spot_url,cookies,TASID,CSRF,0)[1]['data']['locations'][0]
            spot_name = response['name']
            print(f'Scraping {spot_name} ({index} of {len(listings)})')
            
            index=index+1

            # Get total review count
            total_reviews = response['reviewListPage']['totalCount']
            # Get number of pages to get all the reviews
            pages = math.ceil(total_reviews / 20)
            print(f"Number of Pages are {pages} and total reviews are {total_reviews}")
            pages = min(MAX_PAGES, pages)


            # Iterate through every possible page to get all the reviews
            for i in range(pages):
                # Sleep random seconds to avoid blocking from Tripadvisor
                time.sleep(random.randint(1, 2))
                # Get the GraphQL response for each page
                print(f"I'm scraping page {i} from {spot_name}")
                response = request_graphql_with_cookies(spot_url,cookies,TASID,CSRF, page=i)[1]['data']['locations'][0]
                # Get the reviews from each response
                reviews = response['reviewListPage']['reviews'] if response['reviewListPage'] is not None else []

                # Add each review to the array
                for review in reviews:
                    review_title = review['title']
                    review_description = review['text']
                    location = review['location']['parent']['additionalNames']['normal']
                    review_data = {
                    'Spot Name': spot_name,
                    'Review Date': review['createdDate'],
                    'Stay Date': review['tripInfo']['stayDate'] if review['tripInfo'] is not None else None,
                    'Location': location,
                    'Lang': review['language'],
                    'Spot Tip': review['roomTip'] if 'roomTip' in review else None,
                    'Review Title': review_title,
                    'Review Stars': review['rating'],
                    'Review': review_description,
                    'User Name': review['userProfile']['displayName'] if review['userProfile'] else None,
                    'Hometown': review['userProfile']['hometown']['location']['additionalNames']['long'] if review['userProfile'] is not None and review['userProfile']['hometown']['location'] is not None else None
                    }

                    # Iterate through additionalRatings (Cleanliness, Room Service...)
                    for rating in review['additionalRatings']:
                        review_data[f'{rating["ratingLabel"]} Stars'] = rating['rating']

                    data.append(review_data)
        except:
            continue   
    print(f'Reviews fetched from the Group {group_index}: {len(data)}')


    #Store alla the reviews in a dataframe (CSV)
    df = pd.DataFrame(data)
    print(f"Original DataFrame for the group {group_index} has: {df.shape[0]}")
    df=df.drop_duplicates()
    print(f"DataFrame wo Duplicates for the group {group_index} has: {df.shape[0]}")
    df.to_csv(f'./{name_dataset}_reviews_part_{group_index}.csv', index=False, encoding='utf-8-sig', sep=';')
    df.head()

print("FINISH: All the groups SCRAPED!")