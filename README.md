# FederatedLearning-Flask-Gunicorn

# Image Analytics using Federated Deep Learning Architecture
Here is the implementation of Federated Deep Learning Architecture for object detection using Flask framework and containerized it using Gunicorn server. It has transfer learning on pre-trained MobileNet model which is a lightweight deep neural network with fewer parameters and higher classification accuracy.  
   For further details, [A Demonstration of Smart Doorbell Design Using Federated Deep Learning](https://arxiv.org/pdf/2010.09687.pdf).  
   
   **Requirements**
   * Python 3.7
   * tensorflow
   * keras
   * matplotlib
   * Scikit-learn
   * OpenCV
   * Flask
   * Gunicorn
   
   ***
   
   ## Image Dataset Directory Structure  
   Arrange your Training Datset in the following directory structure:  
   ![Dataset directory structure](https://github.com/ResearchTrio/federatedlearning/blob/main/dataset_directory1.png)  
   ***
   
   ## Run the system using the steps below:  
   ### Booting Up
   1. Navigate to device1 directory and run Device 1 using
   ```
   gunicorn --bind localhost:8001 --timeout 600 wsgi1:app
   ```
   2. Navigate to device2 directory and run Device 2 using
   ```
   gunicorn --bind localhost:8002 --timeout 600 wsgi2:app
   ```
   3. Navigate to main_server directory and run Main Server using
   ```
   gunicorn --bind localhost:8000 --timeout 600 wsgi3:app
   ```
   This will start the Gunicorn servers for Device 1 ,Device 2 and Main Server
   
   ##### Servers:
   * Main Server - ```http://localhost:8000/```
   
   ![Main Server Start](https://github.com/ResearchTrio/federatedlearning/blob/main/server_start.png)
   
   * Device 1 - ```http://localhost:8001/```
   * Device 2 - ```http://localhost:8002/```
   
   ![Device Start](https://github.com/ResearchTrio/federatedlearning/blob/main/device_start.png)
   
   ##### System Working
   1. First a model is trained locally on the device. Click on the **```Model Training (Locally)```** button to start model training. This button will send ```http://localhost:8001/modeltrain``` and ```http://localhost:8002/modeltrain``` requests respectively to train models locally.
   
   2. Once the models are trained, click on  **```Send Model to Federated Server```** button. This will send the client models trained on the local devices to the main server using ```http://localhost:8001/sendmodel``` an ```http://localhost:8001/sendmodel``` requests respectively.
   
   3. The trained models sent by the local devices are stored on the Main Server. Now click on **```Aggregate Local Models```** button that sends ```http://localhost:8000/aggregate_models``` request to start model aggregation of the locally trained models.
   
   4. Now, once the model aggregation is done, click on **```Send Aggregated Models to Federated Clients```** button that sends ```http://localhost:8000/send_model_clients``` request to send the global aggregated model back to the local devices.
   
   5. Once the complete iteration is finished go back to step one for the next iteration of model training and aggregation to improve the aggregated model.
   
