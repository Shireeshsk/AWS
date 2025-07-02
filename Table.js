import { DynamoDBClient } from "@aws-sdk/client-dynamodb";
import { DynamoDBDocumentClient, PutCommand } from "@aws-sdk/lib-dynamodb";

const client = new DynamoDBClient({});
const dynamo = DynamoDBDocumentClient.from(client);

export const handler = async (event) => {
  let body;
  try {
    body = JSON.parse(event.body);
  } catch (e) {
    return {
      statusCode: 400,
      body: JSON.stringify({ error: "Invalid JSON" }),
    };
  }

  const params = {
    TableName: "FeedbackTable",
    Item: {
      rollno: body.rollno,
      name: body.name,
      subject: body.subject,
      rating: body.rating,
    },
  };

  try {
    await dynamo.send(new PutCommand(params));
    return {
      statusCode: 200,
      headers: {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Allow-Methods": "OPTIONS,POST",
      },
      body: JSON.stringify({ message: "Success" }),
    };
  } catch (err) {
    console.error("DynamoDB insert error", err);
    return {
      statusCode: 500,
      body: JSON.stringify({ error: "Could not write to DynamoDB" }),
    };
  }
};
