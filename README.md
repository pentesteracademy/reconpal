![0](https://user-images.githubusercontent.com/25884689/169852572-c774ead7-069b-4d35-abcb-a52e349144f2.png)

# ReconPal: Leveraging NLP for Infosec
Recon is one of the most important phases that seem easy but takes a lot of effort and skill to do right. One needs to know about the right tools, correct queries/syntax, run those queries, correlate the information, and sanitize the output. All of this might be easy for a seasoned infosec/recon professional to do, but for rest, it is still near to magic. How cool it will be to ask a simple question like "Find me an open Memcached server in Singapore with UDP support?" or "How many IP cameras in Singapore are using default credentials?" in a chat and get the answer?

The integration of GPT-3, deep learning-based language models to produce human-like text, with well-known recon tools like Shodan, is the foundation of ReconPal. ReconPal also supports using voice commands to execute popular exploits and perform reconnaissance.

## Built With

* OpenAI GPT-3
* Shodan API
* Speech-to-Text
* Telegram Bot
* Docker Containers
* Python 3


# Getting Started

To get ReconPal up and running, follow these simple steps.

### Prerequisites

* Telegram Bot Token
Use BotFather and create a new telegram bot. Refer to the documentation at https://core.telegram.org/bots
* Shodan API:  
Create a shodan Account and create a new API Key from https://account.shodan.io/
* Google Speech-to-Text API:  
Enable Speech-to-Text in GCP and get the credentials. Refer to these steps from the documentation https://cloud.google.com/speech-to-text/docs/before-you-begin
* OpenAI API Key:  
Create a free openAI account to try out the API. https://beta.openai.com/account/api-keys
* Docker

  ```sh
  sudo apt-get updates​
  sudo apt-get install docker.io​
  sudo curl -L "https://github.com/docker/compose/releases/download/1.26.0/docker-compose-$(uname -s)-$(uname -m)" -o​ /usr/local/bin/docker-compose​
  chmod +x /usr/local/bin/docker-compose
  ```

### Installation

1. Clone the repo

   ```sh
   git clone https://github.com/pentesteracademy/reconpal.git
   ```

2. Enter your OPENAI, SHODAN API keys, and TELEGRAM bot token in `docker-compose.yml`

   ```yml
   OPENAI_API_KEY=<Your key>
   SHODAN_API_KEY=<Your key>
   TELEGRAM_BOT_TOKEN=<Your token>
   ```

3. Start reconpal

   ```sh
   docker-compose up
   ```

# Usage

Open the telegram app and select the created bot to use ReconPal.

1. Click on start or just type in the input box.

```
/start
```

2. Register the model.

```
/register
```

3. Test the tool with some commands.

```
scan 10.0.0.8
```

# Tool featured at

- Blackhat Asia Arsenal 2022 <https://www.blackhat.com/asia-22/arsenal/schedule/#reconpal-leveraging-nlp-for-infosec-26232>

- Demonstration Video <https://www.youtube.com/watch?v=gBQFlirFqpk>

# Contributors

Jeswin Mathai, Senior Security Researcher, INE  <jmathai@ine.com>

Nishant Sharma, Security Research Manager, INE <nsharma@ine.com>

Shantanu Kale, Cloud Developer, INE  <skale@ine.com>

Sherin Stephen, Cloud Developer, INE  <sstephen@ine.com>

Sarthak Saini (Ex-Pentester Academy) 

# Documentation

For more details, refer to the "ReconPal.pdf" PDF file. This file contains the slide deck used for presentations.


# Screenshots

Starting reconpal and registering model

![1](https://user-images.githubusercontent.com/25884689/169850014-ea2dd47a-327c-4bd0-8e5e-3ab3cad2e102.png)

Finder module in action

![2](https://user-images.githubusercontent.com/25884689/169850035-f278f58a-78d6-4ebb-b6da-8cf26a472f93.png)

Scanner module in action

![3](https://user-images.githubusercontent.com/25884689/169850066-cbc498f3-9a0f-4bb0-bc2d-88c5b0d576bb.png)

Attacker module in action

![4](https://user-images.githubusercontent.com/25884689/169851366-818b52c9-64c3-46fe-8c3b-76e3cb2105fb.png)

Voice Support

![5](https://user-images.githubusercontent.com/25884689/169850168-8c6d74ec-9ed8-47b8-adc9-463c60edc628.png)

# License

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License v2 as published by the Free Software Foundation.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <http://www.gnu.org/licenses/>.