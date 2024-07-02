# Use official python image as base
FROM public.ecr.aws/lambda/python:3.12

# Setup wok directory
WORKDIR /Share_app_aws

# Copy requirements file
COPY requirements.txt .

# Install packages from requirements.txt
RUN pip install -r requirements.txt

# Copy contents
COPY . .

# Command to run at container start
CMD ["main.lambda_handler" ]
