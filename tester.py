import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from tqdm import tqdm

#  answer[v.get_attribute("innerText")] = None

if __name__ == "__main__":
    driver = webdriver.Chrome("~/Desktop/chromedriver.exe")
    driver.get("https://uva-bi-sdad.github.io/community_example/")
    time.sleep(5)

    dropdowns = ["selected_variable", "selected_district", "selected_county"]

    reset = driver.find_element(By.ID, "reset.selection")

    var_dropdown = driver.find_element(By.ID, "selected_variable")
    vars = driver.find_element(By.ID, "selected_variable-listbox").find_elements(
        By.XPATH,
        './/div[contains(@role,"option") and contains(@class,"combobox-option") and not(contains(@class,"hidden")) ]',
    )

    print("Number of variables: %s" % len(vars))

    click_time = 0.5
    # For each variable
    for v in tqdm(vars):
        var_dropdown.click()
        time.sleep(click_time)
        v.click()

        dis_dropdown = driver.find_element(By.ID, "selected_district")
        dis = driver.find_element(By.ID, "selected_district-listbox").find_elements(
            By.XPATH,
            './/div[contains(@role,"option") and contains(@class,"combobox-option") and not(contains(@class,"hidden")) ]',
        )
        time.sleep(click_time)
        # For each district
        for d in tqdm(dis):
            # need to clear the county selection to itereate
            dis_dropdown.click()
            time.sleep(click_time)
            d.click()

            time.sleep(click_time)
            con_dropdown = driver.find_element(By.ID, "selected_county")
            clear_button = driver.find_element(By.ID, "selected_county").find_element(
                By.XPATH, './/button[contains(@class,"btn-close")]'
            )
            cons = driver.find_element(By.ID, "selected_county-listbox").find_elements(
                By.XPATH,
                './/div[contains(@role,"option") and contains(@class,"combobox-option") and not(contains(@class,"hidden")) ]',
            )
            # For each county
            for c in tqdm(cons):
                con_dropdown.click()
                time.sleep(click_time)
                c.click()
                key = "%s,%s,%s" % (
                    v.get_attribute("innerText"),
                    d.get_attribute("innerText"),
                    c.get_attribute("innerText"),
                )
                time.sleep(5)
                summary = driver.find_element(By.CLASS_NAME, "info-summary")
                val = sum(
                    [
                        float(x)
                        for x in summary.get_attribute("innerText")
                        .split("\n")[-1]
                        .split("\t")
                    ]
                )
                with open("trace.txt", "a") as f:
                    f.write("%s, %s\n" % (key, val))
                # You need to clear the selection in order to iterate on the district
                clear_button.click()
                time.sleep(click_time)
        reset.click()
    driver.close()
