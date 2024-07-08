# Use official python image as base
FROM public.ecr.aws/lambda/python:3.12

# Copy requirements file
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Install packages from requirements.txt
RUN pip install -r ${LAMBDA_TASK_ROOT}/requirements.txt

# Copy contents
COPY . ${LAMBDA_TASK_ROOT}

# Command to run at container start
CMD ["main.lambda_handler" ]
