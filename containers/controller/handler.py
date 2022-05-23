from shodan import Shodan
from websocket import create_connection
import os
import openai

api = Shodan(os.getenv("SHODAN_API_KEY"))
openai.api_key = os.getenv("OPENAI_API_KEY")
REGISTER_FLAG = 0
trained_model_name = ""


class Controller:
    """Class to encapsulate reconpal logic"""

    def scan(command, update):
        """Communicate with Scanner module"""
        print("trying connection")
        ws = create_connection("ws://10.131.131.4:49000")
        print("Started Connection")
        ws.send(command)
        for message in ws:
            if message == "--END--":
                break
            else:
                # Split message according to max telegram message length
                if len(message) > 4096:
                    for x in range(0, len(message), 4096):
                        update.message.reply_text(
                            message[x: x + 4096] + "\n",
                            disable_web_page_preview=True,
                        )
                else:
                    update.message.reply_text(
                        message + "\n", disable_web_page_preview=True
                    )

        ws.close()
        update.message.reply_text("Done \U0001F601\n")

    def attack(command, update):
        """Communicate with Attacker module"""
        print("trying connection")
        ws = create_connection("ws://10.131.131.6:50000")
        print("Started Connection")
        ws.send(command)
        for message in ws:
            if message == "--END--":
                break
            else:
                # Split message according to max telegram message length
                if len(message) > 4096:
                    for x in range(0, len(message), 4096):
                        update.message.reply_text(
                            message[x: x + 4096] + "\n",
                            disable_web_page_preview=True,
                        )
                else:
                    update.message.reply_text(
                        message + "\n", disable_web_page_preview=True
                    )

        ws.close()
        update.message.reply_text("Done \U0001F601\n")

    def process_input(self, raw_input, update):
        """Process input received from telegram"""
        query = ""
        global trained_model_name, REGISTER_FLAG
        if REGISTER_FLAG == 0:
            # Check if OpenAI model has been registered
            update.message.reply_text("Please register model with /register\n")
        elif raw_input.startswith(">"):
            # Process custom commands
            Controller.scan(raw_input[2:], update)
        else:
            update.message.reply_text("Processsing.. Please wait!\n")
            # Generate text to code completion
            full_response = openai.Completion.create(
                model=trained_model_name,
                prompt=[raw_input + "\n"],
                temperature=0,
                max_tokens=100,
                top_p=1,
                frequency_penalty=0.2,
                presence_penalty=0,
                stop=["\n"],
            )
            response_text = full_response["choices"][0]["text"]
            selected_module = response_text[: response_text.find("~")]
            response_text = response_text[response_text.find("~") + 1:]

            # Route commands to appropriate modules
            if selected_module == "scanner":
                update.message.reply_text(
                    "Interpreted command: " + response_text
                )
                Controller.scan(response_text, update)
            elif selected_module == "finder":
                query = response_text
                """Temporary fix for incorrect openAI response"""
                count_rep = query.count("country")
                if count_rep > 1:
                    c_index = query.find("country")
                    query = query[: c_index + 12]

                update.message.reply_text("Interpreted command: " + query)
                dump = api.search(
                    query,
                    page=None,
                    limit=None,
                    offset=8,
                    facets=None,
                    minify=True,
                )

                if query.find("search") != -1:
                    query = query.replace("shodan search", " ")
                    query = query.strip()
                    dump = api.search(query)
                    update.message.reply_text(
                        "Total Results: " + str(len(dump["matches"])) + " \n"
                    )
                    for match in dump["matches"]:
                        update.message.reply_text(
                            "{}\n".format(
                                (
                                    "IP: {}\nOS: {}\nISP: {}\nRegion Code: {}\
                                        \nCity Name: {}\
                                        \nCountry Name: {}".format(
                                        match["ip_str"],
                                        match["os"],
                                        match["isp"],
                                        match["location"]["region_code"],
                                        match["location"]["city"],
                                        match["location"]["country_name"],
                                    )
                                )
                            )
                        )
                    update.message.reply_text("Done \U0001F601\n")
                elif query.find("host") != -1:
                    update.message.reply_text("Interpreted command: " + query)
                    query = query.replace("shodan host", " ")
                    query = query.strip()
                    dump = api.host(query)
                    update.message.reply_text(
                        "{}\n".format(
                            (
                                "IP: {}\nOS: {}\nISP: {}\nHostname: {}\
                                    \nPorts: {}\nCity Name: {}\
                                    \nCountry Name: {}".format(
                                    dump["ip_str"],
                                    dump["os"],
                                    dump["isp"],
                                    dump["hostnames"],
                                    dump["ports"],
                                    dump["city"],
                                    dump["country_name"],
                                )
                            )
                        )
                    )
                    update.message.reply_text("Done \U0001F601\n")
                else:
                    update.message.reply_text(
                        "Sorry ReconPal is unable to understand your \
                            request \U0001F61E\n"
                    )

            elif selected_module == "attacker":
                update.message.reply_text(
                    "Interpreted command: " + response_text
                )
                Controller.attack(response_text, update)

            else:
                update.message.reply_text(
                    "Sorry ReconPal is unable to understand your \
                        request \U0001F61E\n"
                )

    def register_commands(self, data, update):
        """Function to upload training file and train model"""
        global trained_model_name, REGISTER_FLAG
        f = open("datastore/model", "r")
        model_name = f.read()
        f.close()
        if model_name[:7] == "davinci":
            # Check if trained model is already available
            trained_model_name = model_name
            update.message.reply_text(
                "Model " + trained_model_name + " in use\n"
            )
            REGISTER_FLAG = 1
        elif model_name[:2] == "ft":
            # Check if model has finished fine tune
            retrieve_response = openai.FineTune.retrieve(id=model_name)
            if retrieve_response["status"] == "succeeded":
                trained_model_name = retrieve_response["fine_tuned_model"]
                update.message.reply_text(
                    "Fine Tuned model created with name\n" + trained_model_name
                )
                f = open("datastore/model", "w")
                f.write(trained_model_name)
                f.close()
                REGISTER_FLAG = 1
            else:
                update.message.reply_text("Please wait for fine tune\n")
        else:
            # Upload dataset for fine tune
            update.message.reply_text("Uploading dataset for fine tune\n")
            file_create_response = openai.File.create(
                file=open("datastore/dataset_reconpal.jsonl"),
                purpose="fine-tune",
            )
            training_file_id = file_create_response["id"]
            finetune_create_response = openai.FineTune.create(
                training_file=training_file_id, model="davinci"
            )
            update.message.reply_text("Started fine-tune\n")

            finetune_id = finetune_create_response["id"]
            f = open("datastore/model", "w")
            f.write(finetune_id)
            f.close()
