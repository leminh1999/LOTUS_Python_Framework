def scanClipAndPushMySQL(lastVideoElementSrc = ""):
  newClipFlag = 0

  #1. Check new video
  videoElement = chrome.driver.find_element(By.XPATH,"//video[contains(@class,'VideoBasic')]")
  videoElementSrc = videoElement.get_attribute('src')
  if videoElementSrc != lastVideoElementSrc: newClipFlag = True
  
  #2. Get clip Info
  if newClipFlag == True:
    fullClipElement = videoElement.find_element(By.XPATH,"./ancestor::div[contains(@data-e2e,'list-item-container')]")
    
    userId       = fullClipElement.find_element(By.XPATH,"./child::*//*[contains(@data-e2e,'video-author-uniqueid')]").text
    userNickname = fullClipElement.find_element(By.XPATH,"./child::*//*[contains(@data-e2e,'video-author-nickname')]").text
    postTime     = fullClipElement.find_element(By.XPATH,"./child::*//*[contains(@class,'StyledAuthorAnchor')]").text.split("·")[1].strip()
    likeCount    = fullClipElement.find_element(By.XPATH,"./child::*//*[@data-e2e='like-count']").text
    commentCount = fullClipElement.find_element(By.XPATH,"./child::*//*[@data-e2e='comment-count']").text
    shareCount   = fullClipElement.find_element(By.XPATH,"./child::*//*[@data-e2e='share-count']").text

    print('-'*50)
    print("UserID  :",userId)
    print("Nickname:",userNickname)
    print("PostTime:",postTime)
    print("Like num:",likeCount)
    print("Commemt :",commentCount)
    print("Share   :",shareCount)
    print("Video   :",videoElementSrc)
    print("")
  #3. Push MySQL
  
  
  if newClipFlag == True:
    return videoElementSrc
  else:
    return lastVideoElementSrc