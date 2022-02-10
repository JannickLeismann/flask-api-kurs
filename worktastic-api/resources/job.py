from flask import request
from flask_restful import Resource
from http import HTTPStatus
from models.job import Job
from flask_jwt_extended import jwt_required, get_jwt_identity


class JobListResource(Resource):

    def get(self):
        data = []

        for job in Job.get_all_published():
            if job.is_published is True:
                data.append(job.data)

        return {'data': data}, HTTPStatus.OK

    @jwt_required()
    def post(self):
        data = request.get_json()

        job = Job(
            title=data['title'],
            description=data['description'],
            salary=data['salary']
        )

        user_id = get_jwt_identity()
        job.user_id = user_id

        job.save()

        return job.data, HTTPStatus.CREATED

class JobResource(Resource):

    def get(self, job_id):

        job = Job.get_by_id(job_id=job_id)

        if job is None:
            return {'message': 'job not found'}, HTTPStatus.NOT_FOUND

        if job.is_published is False:
            return {'message': 'job not published'}, HTTPStatus.FORBIDDEN

        return job.data, HTTPStatus.OK

    @jwt_required()
    def put(self, job_id):
        data = request.get_json()

        job = Job.get_by_id(job_id=job_id)

        if job is None:
            return {'message': 'job not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if job.user_id != current_user:
            return {'message': 'access denied'}, HTTPStatus.FORBIDDEN

        job.title = data['title']
        job.description = data['description']
        job.salary = data['salary']

        job.save()

        return job.data, HTTPStatus.OK

    @jwt_required()
    def delete(self, job_id):

        job = Job.get_by_id(job_id=job_id)

        if job is None:
            return {'message': 'job not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if job.user_id != current_user:
            return {'message': 'access denied'}, HTTPStatus.FORBIDDEN

        job.delete()

        return {}, HTTPStatus.NO_CONTENT


class JobPublishResource(Resource):

    @jwt_required()
    def put(self, job_id):

        job = Job.get_by_id(job_id=job_id)

        if job is None:
            return {'message': 'job not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if job.user_id != current_user:
            return {'message': 'access denied'}, HTTPStatus.FORBIDDEN

        job.is_published = True
        job.save()

        return {}, HTTPStatus.OK

    @jwt_required()
    def delete(self, job_id):

        job = Job.get_by_id(job_id=job_id)

        if job is None:
            return {'message': 'job not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if job.user_id != current_user:
            return {'message': 'access denied'}, HTTPStatus.FORBIDDEN

        job.is_published = False
        job.save()

        return {}, HTTPStatus.OK

