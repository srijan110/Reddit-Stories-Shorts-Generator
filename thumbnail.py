from selenium import webdriver
from selenium.webdriver.common.by import By

preprocessing_page = """
function deleteByXPath(xpath) {
  const result = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null);
  const node = result.singleNodeValue;
  if (node) node.remove();
}
deleteByXPath("//*[@id='credential_picker_container']");
deleteByXPath("/html/body/shreddit-app/div[3]/div/div/main/shreddit-post/div[3]/div");
"""

def get_thumbnail(url="", id="", image_path="files\\image.png"):
    driver = webdriver.Firefox()
    driver.set_window_size(568, 768)

    driver.get(url)

    driver.execute_script(preprocessing_page)

    element = driver.find_element(By.XPATH, f"//*[@id='t3_{id}']")
    element.screenshot(image_path)

    driver.quit()

