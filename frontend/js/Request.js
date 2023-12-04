class Request
{
	constructor(endpoint)
	{
		this.endpoint = endpoint;
		this.headers = {
			'Content-Type': 'application/json',
			'Accept': 'application/json'
		};
	}

	get(url, data = null)
	{
		url = this.endpoint + url;
		return fetch(url, {
			method: 'GET',
			headers: this.headers,			
		});
	}

	post(url, data = null)
	{
		url = this.endpoint + url;
		return fetch(url, {
			method: 'POST',
			headers: this.headers,
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