class Request
{
	constructor(endpoint)
	{
		this.endpoint = endpoint;
		this.get_headers = {
			'Accept': 'application/json',
			'Content-Type': 'application/json'
		}

		this.post_headers = {
			'Content-Type': 'application/json',
			'Accept': 'application/json'
		};
	}

	get(url, data = null)
	{
		url = this.endpoint + url;
		var headers = this.get_headers;
		return fetch(url, {
			method: 'GET',
			headers: headers,			
		});
	}

	post(url, data = null)
	{
		url = this.endpoint + url;
		var headers = this.post_headers;
		return fetch(url, {
			method: 'POST',
			headers: headers,
			body: JSON.stringify(data)
		});
	}

	put(url, data = null)
	{
		url = this.endpoint + url;
		return fetch(url, {
			method: 'PUT',
			headers: this.headers,
			body: JSON.stringify(data)
		});
	}

	delete(url, data=null)
	{
		url = this.endpoint + url;
		return fetch(url, {
			method: 'DELETE',
			headers: this.headers,
			body: JSON.stringify(data)
		});
	}
}

export default Request;